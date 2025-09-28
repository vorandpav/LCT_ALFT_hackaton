import React from "react";

interface Box {
    box_id: string;
    predicted_class: string;
    confidence: number;
    possible_tools: string[];
}

interface Props {
    boxes: Box[];
    onConfirm: (boxId: string, toolId: number) => void;
    onDelete: (boxId: string) => void;
}

export default function WorkTable({boxes, onConfirm, onDelete}: Props) {
    return (
        <table className="table-auto border-collapse border border-gray-400 w-full">
            <thead>
            <tr className="bg-gray-100">
                <th>Box ID</th>
                <th>Class</th>
                <th>Confidence</th>
                <th>Варианты</th>
                <th>Действия</th>
            </tr>
            </thead>
            <tbody>
            {boxes.map((box) => (
                <tr key={box.box_id} className="border">
                    <td>{box.box_id}</td>
                    <td>{box.predicted_class}</td>
                    <td>{Math.round(box.confidence * 100)}%</td>
                    <td>
                        <select
                            onChange={(e) => onConfirm(box.box_id, parseInt(e.target.value))}
                        >
                            <option value="">Выбрать...</option>
                            {box.possible_tools.map((tool, idx) => (
                                <option key={idx} value={idx}>
                                    {tool}
                                </option>
                            ))}
                        </select>
                    </td>
                    <td>
                        <button
                            onClick={() => onDelete(box.box_id)}
                            className="bg-red-500 text-white px-2 py-1 rounded"
                        >
                            Удалить
                        </button>
                    </td>
                </tr>
            ))}
            </tbody>
        </table>
    );
}
