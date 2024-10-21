export function getFormattedDate(s: string | undefined) {
    if (typeof s === "string") {
        const date = new Date(Date.parse(s));
        return date.toLocaleDateString('ru-RU');
    }
}

export function daysBetween(start: string, end: string) {
    const res = Date.parse(end) - Date.parse(start);
    return res / (1000 * 60 * 60 * 24);
}
