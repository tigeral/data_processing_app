import { useState, useCallback } from "react";
import type { DragEvent } from "react";
import type { DroppedItem } from "../utils/detectDroppedItems";
import { detectDroppedItems } from "../utils/detectDroppedItems";
import { sendDrops } from "../utils/dropsApi";
import "./DropZone.css";

interface LogEntry {
  id: number;
  items: DroppedItem[];
  timestamp: string;
  error?: string;
}

let nextId = 0;

export function DropZone() {
  const [isDragOver, setIsDragOver] = useState(false);
  const [log, setLog] = useState<LogEntry[]>([]);

  const handleDragOver = useCallback((e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  }, []);

  const handleDragEnter = useCallback((e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: DragEvent<HTMLDivElement>) => {
    // Only clear if leaving the zone itself, not a child element
    if (!e.currentTarget.contains(e.relatedTarget as Node)) {
      setIsDragOver(false);
    }
  }, []);

  const handleDrop = useCallback(async (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);

    const items = await detectDroppedItems(e.dataTransfer);
    console.log("[DropZone] dropped items:", items);

    const entry: LogEntry = {
      id: nextId++,
      items,
      timestamp: new Date().toLocaleTimeString(),
    };

    try {
      await sendDrops(items);
    } catch (err) {
      entry.error = err instanceof Error ? err.message : String(err);
      console.error("[DropZone] backend error:", entry.error);
    }

    setLog((prev) => [entry, ...prev]);
  }, []);

  return (
    <div className="drop-zone-wrapper">
      <div
        className={`drop-zone${isDragOver ? " drop-zone--active" : ""}`}
        onDragOver={handleDragOver}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {isDragOver
          ? "Release to drop"
          : "Drag and drop files, folders, URLs, or images here"}
      </div>

      {log.length > 0 && (
        <div className="drop-log">
          <h2>Drop Log</h2>
          {log.map((entry) => (
            <div key={entry.id} className="drop-log__entry">
              <span className="drop-log__time">{entry.timestamp}</span>
              {entry.error && (
                <span className="drop-log__error">Backend error: {entry.error}</span>
              )}
              <ul>
                {entry.items.map((item, idx) => (
                  <li key={idx} className={`drop-log__item drop-log__item--${item.type}`}>
                    <span className="drop-log__badge">{item.type}</span>
                    <span className="drop-log__name">{item.name}</span>
                    {item.mime_type && (
                      <span className="drop-log__meta">{item.mime_type}</span>
                    )}
                    {item.size !== undefined && (
                      <span className="drop-log__meta">{item.size.toLocaleString()} B</span>
                    )}
                    {item.children && (
                      <span className="drop-log__meta">
                        {item.children.length} item(s): {item.children.join(", ")}
                      </span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
