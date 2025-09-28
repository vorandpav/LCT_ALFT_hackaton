import React, {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import {getWork, scanGiving, confirmBox, completeGiving} from "../api/works";
import WorkTable from "../components/WorkTable";

export default function Work() {
    const {workId} = useParams<{ workId: string }>();
    const [work, setWork] = useState<any>(null);
    const [boxes, setBoxes] = useState<any[]>([]);

    useEffect(() => {
        if (workId) {
            getWork(parseInt(workId)).then(setWork);
        }
    }, [workId]);

    const handleScan = async () => {
        if (workId) {
            const result = await scanGiving(parseInt(workId));
            setBoxes(result.detections || []);
        }
    };

    const handleConfirm = (boxId: string, toolId: number) => {
        if (workId) {
            confirmBox(parseInt(workId), boxId, toolId);
        }
    };

    const handleComplete = async () => {
        if (workId) {
            await completeGiving(parseInt(workId));
            alert("Выдача завершена!");
        }
    };

    return (
        <div className="p-4">
            <h1 className="text-xl font-bold">Работа #{workId}</h1>
            <button
                onClick={handleScan}
                className="bg-green-500 text-white px-4 py-2 rounded m-2"
            >
                Сканировать
            </button>
            <WorkTable boxes={boxes} onConfirm={handleConfirm} onDelete={() => {
            }}/>
            <button
                onClick={handleComplete}
                className="bg-blue-500 text-white px-4 py-2 rounded m-2"
            >
                Завершить выдачу
            </button>
        </div>
    );
}
