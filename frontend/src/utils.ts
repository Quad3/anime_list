export function getFormattedDate(s: string | undefined) {
    if (typeof s === "string") {
        const date = new Date(Date.parse(s))
        return date.toLocaleDateString('ru-RU')
    }
}
