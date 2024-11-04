import { useRef, useEffect } from "react";

export function useHorizontalScroll() {
    const elRef = useRef<HTMLDivElement>(null);
    useEffect(() => {
        const multiplier = 3;
        const el = elRef.current;
        if (el) {
            const onWheel = (e: { deltaY: number; preventDefault: () => void; }) => {
                if (e.deltaY === 0) return;
                e.preventDefault();
                el.scrollTo({
                    left: el.scrollLeft + e.deltaY * multiplier,
                    behavior: "smooth",
                });
            };
            el.addEventListener("wheel", onWheel);
            return () => el.removeEventListener("wheel", onWheel);
        }
    }, []);
    return elRef;
}
