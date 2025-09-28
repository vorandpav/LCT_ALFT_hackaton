import React, {useState} from "react";
import {useNavigate} from "react-router-dom";

export default function Home() {
    const [workId, setWorkId] = useState("");
    const navigate = useNavigate();

    return (
        <div className="p-4">
            <h1 className="text-xl font-bold">Выбор работы</h1>
            <input
                className="border p-2 m-2"
                placeholder="Введите work_id"
                value={workId}
                onChange={(e) => setWorkId(e.target.value)}
            />
            <button
                className="bg-blue-500 text-white px-4 py-2 rounded"
                onClick={() => navigate(`/work/${workId}`)}
            >
                Перейти
            </button>
        </div>
    );
}
