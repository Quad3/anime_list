import React, {useEffect, useState} from 'react';

import {daysBetween} from "../../../utils";
import {
    StartEnd,
    Line,
    Text,
    StartEndListResponse,
    ComplexRect,
} from "./Models";
import cl from './Gantt.module.css';
import AnimeListService from "../../../services/AnimeListService";
import {useHorizontalScroll} from "./HorizontalScroll";

const COLUMN_WIDTH = 50;
const ROW_HEIGHT = 50;
const DAYS_GAP = 7;

let GRID_WIDTH = 0;
let ROW_NUMBER = 0;
let GRID_HEIGHT = 0;
let STATE_STYLES: {[index: string]: any} = {
    WATCHED: cl.stateWatched,
    WATCHING: cl.stateWatching,
    DROPPED: cl.stateDropped,
};

const Gantt = () => {
    const [animeList, setAnimeList] = useState<StartEndListResponse[]>([]);
    const [dateSegments, setDateSegments] = useState<StartEnd[]>([]);
    const [columnLines, setColumnLines] = useState<Line[]>([]);
    const [rowLines, setRowLines] = useState<Line[]>([]);
    const [days, setDays] = useState<Text[]>([]);
    const [months, setMonths] = useState<Text[]>([]);
    const [xOffsets, setXOffsets] = useState<number[]>([]);
    const [animeRects, setAnimeRects] = useState<ComplexRect[]>([]);
    const [animeTitles, setAnimeTitles] = useState<Text[]>([]);
    const scrollRef = useHorizontalScroll();

    async function fetchAnimeList() {
        try {
            const response = await AnimeListService.getStartEndList();
            setAnimeList(response.data);
        } catch (e: any) {
            console.log(e.response?.data?.detail);
        }
    }

    useEffect(() => {
        fetchAnimeList();
    }, []);

    useEffect(() => {
        if (animeList.length !== 0)
            setDateSegments(getDateSegments());
    }, [animeList]);

    useEffect(() => {
        if (dateSegments.length !== 0) {
            GRID_WIDTH = getGridWidth();
            setDays(getDays());
            setMonths(getMonths());
            setXOffsets(getXOffsets());
        }
    }, [dateSegments]);

    useEffect(() => {
        if (xOffsets.length !== 0) {
            setAnimeRects(getAnimeRectsAndRowNumber());
            setRowLines(getRowLines());
            GRID_HEIGHT = ROW_HEIGHT * ROW_NUMBER;
            setColumnLines(getColumnLines());
        }
    }, [xOffsets]);

    useEffect(() => {
        if (animeRects.length !== 0) {
            setAnimeTitles(getAnimeTitles());
            setScrollOnRight();
        }
    }, [animeRects]);

    function setScrollOnRight() {
        window.document.getElementById('gantt')?.scrollTo({left: GRID_WIDTH});
    }

    function getDateSegments() {
        let res: StartEnd[] = [];

        let cur_start = animeList[0].start_date;
        let cur_end = animeList[0].end_date;
        for (let i=0; i<animeList.length; i++) {
            if (
                cur_end.localeCompare(animeList[i].start_date) < 0 &&
                daysBetween(cur_end, animeList[i].start_date) > DAYS_GAP
            ) {
                res.push({start_date: cur_start, end_date: cur_end});
                cur_end = animeList[i].end_date
                cur_start = animeList[i].start_date;
            } else {
                cur_end = cur_end.localeCompare(animeList[i].end_date) < 0
                    ? animeList[i].end_date
                    : cur_end;
            }
        }
        res.push({start_date: cur_start, end_date: cur_end});
        return res
    }

    function getGridWidth() {
        let curX = 0;
        dateSegments.map((dateSegment, index) => {
            curX += COLUMN_WIDTH * (daysBetween(dateSegment.start_date, dateSegment.end_date) + 1);
            if (index !== dateSegments.length - 1) {
                curX += COLUMN_WIDTH * 2;
            }
        });
        return curX;
    }

    function getColumnLines() {
        let lines: Line[] = [];

        let curX = 0;
        dateSegments.map((dateSegment, index) => {
            for (let i=0; i<=daysBetween(dateSegment.start_date, dateSegment.end_date); i++) {
                lines.push({x1: curX, y1: 0, x2: curX, y2: GRID_HEIGHT})
                curX += COLUMN_WIDTH;
            }
            if (index !== dateSegments.length - 1) {
                lines.push({x1: curX, y1: 0, x2: curX, y2: GRID_HEIGHT});
                curX += COLUMN_WIDTH * 2;
                lines.push({x1: curX, y1: 0, x2: curX, y2: GRID_HEIGHT});
            }
        });
        lines.push({x1: curX, y1: 0, x2: curX, y2: GRID_HEIGHT});

        return lines
    }

    function getRowLines() {
        let rowLines: Line[] = [];

        for (let i=0; i<ROW_NUMBER + 1; i++)
            rowLines.push({
                x1: 0,
                y1: i * ROW_HEIGHT,
                x2: GRID_WIDTH,
                y2: i * ROW_HEIGHT,
            });

        return rowLines;
    }

    function getDays() {
        const daysOfWeek = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
        const y = ROW_HEIGHT - 5;

        let days: Text[] = [];
        let curX = 0;
        dateSegments.map((dateSegment, index) => {
            let curDate = new Date(Date.parse(dateSegment.start_date));
            for (let i=0; i<=daysBetween(dateSegment.start_date, dateSegment.end_date); i++) {
                let dateAndWeekday = [curDate.getDate(), daysOfWeek[curDate.getDay()]].join(' ');
                days.push({
                    x: curX + COLUMN_WIDTH / 2,
                    y: y,
                    value: dateAndWeekday,
                });
                curDate.setDate(curDate.getDate() + 1);
                curX += COLUMN_WIDTH;
            }
            if (index !== dateSegments.length - 1) {
                curX += COLUMN_WIDTH * 2;
                days.push({
                    x: curX,
                    y: y,
                    value: '',
                });
            }
        });
        return days;
    }

    function getMonths() {
        const monthNames = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
        const shortMonthNames = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
                                 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'];
        const y = ROW_HEIGHT - 25;

        let months: Text[] = [];
        let curX = 0;

        dateSegments.map((dateSegment) => {
            let startDate = new Date(Date.parse(dateSegment.start_date));
            let endDate = new Date(Date.parse(dateSegment.end_date));
            let monthDiff = endDate.getMonth() - startDate.getMonth() + 1;
            let monthStart = new Date(startDate), monthEnd = new Date(startDate);

            for (let i=0; i<monthDiff; i++) {
                if (i !== monthDiff - 1) {
                    monthEnd.setMonth(monthEnd.getMonth() + 1);
                    monthEnd.setDate(0);
                } else {
                    monthEnd = new Date(endDate);
                }

                let daysWidth = monthEnd.getDate() - monthStart.getDate() + 1
                let width = COLUMN_WIDTH * daysWidth;
                let monthValue = daysWidth === 1
                    ? shortMonthNames[monthStart.getMonth()]
                    : monthNames[monthStart.getMonth()];
                months.push({
                    x: curX + width / 2,
                    y: y,
                    value: `${monthValue} ${monthEnd.getFullYear().toString().slice(2)}`,
                });

                curX += width;
                monthStart = new Date(monthEnd);
                monthStart.setDate(monthStart.getDate() + 1);
                monthEnd.setDate(1);
                monthEnd.setMonth(monthEnd.getMonth() + 1);
            }
            curX += COLUMN_WIDTH * 2;
        });

        return months
    }

    function getAnimeRectsAndRowNumber() {
        const complexRects = getComplexAnimeRects();
        ROW_NUMBER = complexRects.length;

        let res: ComplexRect[] = [];
        complexRects.map(arr => {
            arr.map(rect => {
                res.push(rect);
            })
        })
        return res;
    }

    function getAnimeTitles() {
        let res: Text[] = [];
        animeRects.map(animeRect => {
            res.push({
                x: animeRect.x + animeRect.width,
                y: animeRect.y + 20,
                value: animeRect.anime.name,
            })
        });
        return res;
    }

    function getComplexAnimeRects() {
        let res: ComplexRect[][] = [];

        animeList.map((anime, index) => {
            getRectByRate(
                res,
                anime,
                xOffsets[index],
                (daysBetween(anime.start_date, anime.end_date) + 1) * COLUMN_WIDTH,
            );
        });

        return res;
    }

    function getRectByRate(
        source: ComplexRect[][],
        newAnime: StartEndListResponse,
        x: number,
        width: number,
    ) {
        const paddingTop = 10;
        const height = ROW_HEIGHT - paddingTop * 2;
        if (source.length === 0) {
            source.push([{
                anime: newAnime,
                x: x + 5,
                y: paddingTop,
                width: width - 10,
                height: height,
            }]);
            return;
        }
        let added = false;

        for (let i=0; i<source.length; i++) {
            if (newAnime.start_date > source[i][source[i].length - 1].anime.end_date) {
                source[i].push({
                    anime: newAnime,
                    x: x + 5,
                    y: i * ROW_HEIGHT + paddingTop,
                    width: width - 10,
                    height: height,
                });
                added = true;
                break;
            }
        }
        if (!added)
            source.push([{
                anime: newAnime,
                x: x + 5,
                y: source.length * ROW_HEIGHT + paddingTop,
                width: width - 10,
                height: height,
            }]);
    }

    function getXOffsets() {
        let xOffsets: number[] = [];
        let curSegment = 0;
        let curOffset = 0;
        let lastOffset = 0;
        animeList.map((anime) => {
            if (anime.end_date <= dateSegments[curSegment].end_date) {
                lastOffset = curOffset + daysBetween(dateSegments[curSegment].start_date, anime.start_date) * COLUMN_WIDTH
                xOffsets.push(lastOffset);
            } else {
                lastOffset = (
                    curOffset +
                    daysBetween(dateSegments[curSegment].start_date, dateSegments[curSegment].end_date) * COLUMN_WIDTH +
                    COLUMN_WIDTH * 3
                );
                curSegment++;
                curOffset = lastOffset;
                xOffsets.push(lastOffset);
            }
        });
        return xOffsets;
    }

    return (
        <main className={cl.main}>
            <div className={cl.gantt} id="gantt" ref={scrollRef}>
                <svg width={GRID_WIDTH} height={ROW_HEIGHT}>
                    <g>
                        {days.map((dayText) => (
                            <text
                                className={cl.svgTextCenter}
                                key={'dayText' + dayText.x}
                                x={dayText.x}
                                y={dayText.y}
                            >
                                {dayText.value}
                            </text>
                        ))}
                    </g>

                    <g>
                        {months.map((month) => (
                            <text
                                className={[cl.svgTextCenter, cl.svgMonthTitles].join(' ')}
                                key={'monthText' + month.x}
                                x={month.x}
                                y={month.y}
                            >
                                {month.value}
                            </text>
                        ))}
                    </g>
                </svg>

                <div>
                    <svg width={GRID_WIDTH} height={GRID_HEIGHT}>
                        <g className={cl.rows}>
                            {animeRects.map((animeRect, index) => (
                                <rect
                                    className={STATE_STYLES[animeList[index].state]}
                                    key={'animeRect' + index}
                                    {...animeRect}
                                ></rect>
                            ))}
                        </g>
                        <g>
                            {animeTitles.map((animeTitle, index) => (
                                <text
                                    className={cl.animeTitle}
                                    key={'animeTitle' + index}
                                    x={animeTitle.x}
                                    y={animeTitle.y}
                                >
                                    {animeTitle.value}
                                </text>
                            ))}
                        </g>
                        <g className={cl.columnLines}>
                            {columnLines.map((line, index) => (
                                <line
                                    key={'line' + index}
                                    x1={line.x1} y1={line.y1} x2={line.x2} y2={line.y2}
                                ></line>
                            ))}
                        </g>
                        <g className={cl.rowLines}>
                            {rowLines.map((line, index) => (
                                <line
                                    key={'rowLine' + index}
                                    x1={line.x1} y1={line.y1} x2={line.x2} y2={line.y2}
                                ></line>
                            ))}
                        </g>
                    </svg>
                </div>
            </div>
        </main>
    );
};

export default Gantt;
