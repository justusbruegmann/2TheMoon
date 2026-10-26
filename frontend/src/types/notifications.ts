export type Notification = {
    id: number;
    title: string;
    message: string;
    status: Status;
    duration: number;
};

export type NotificationInput = {
    title: string;
    message: string;
    status: Status;
    duration?: number;
};
export type Status = "success" | "error" | "info" | "warning";
