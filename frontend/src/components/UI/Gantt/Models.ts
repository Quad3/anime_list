export interface StartEndListResponse {
    start_date: string,
    end_date: string,
    name: string,
    state: string,
    rate: number,
    review: string,
    user_id: string,
    anime_id: string,
}

export interface StartEnd {
    start_date: string,
    end_date: string,
}

export interface Line {
    x1: number,
    y1: number,
    x2: number,
    y2: number,
}

export interface ComplexRect {
    anime: StartEndListResponse,
    x: number,
    y: number,
    width: number,
    height: number,
}

export interface Text {
    x: number,
    y: number,
    value: string,
}
