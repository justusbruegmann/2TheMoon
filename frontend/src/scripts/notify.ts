import {ref} from "vue";
import type {Notification, NotificationInput, Status} from "../types/notifications.ts";

let nextId = 0;

const durationTimes: Record<Status, number> = {
    success: 3000,
    error: 5000,
    info: 4000,
    warning: 4000,
};

export const notifications = ref<Notification[]>([]);

export function add(notification: NotificationInput) {
    const newNotification: Notification = {
        ...notification,
        id: nextId++,
        duration: notification.duration ?? durationTimes[notification.status],
    };

    notifications.value.push(newNotification);

    setTimeout(() => {
        remove(newNotification.id);
    }, newNotification.duration);
}

export function remove(id: number) {
    notifications.value = notifications.value.filter(
        (notification:Notification) => notification.id !== id,
    );
}

export const notify = {
    success(title: string, message: string, duration: number) {
        add({ title, message, status: "success", duration });
    },

    error(title: string, message: string, duration?: number) {
        add({ title, message, status: "error", duration });
    },

    info(title: string, message: string, duration?: number) {
        add({ title, message, status: "info", duration });
    },

    warning(title: string, message: string, duration?: number) {
        add({ title, message, status: "warning", duration });
    },
};
