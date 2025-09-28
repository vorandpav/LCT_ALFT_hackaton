import api from "./client";

export async function getWork(workId: number) {
    const resp = await api.get(`/works/${workId}`);
    return resp.data;
}

export async function scanGiving(workId: number) {
    const resp = await api.post(`/works/${workId}/scan_giving`);
    return resp.data;
}

export async function confirmBox(workId: number, boxId: string, toolId: number) {
    const resp = await api.post(`/works/${workId}/confirm_box`, {boxId, toolId});
    return resp.data;
}

export async function completeGiving(workId: number) {
    const resp = await api.post(`/works/${workId}/complete_giving`);
    return resp.data;
}
