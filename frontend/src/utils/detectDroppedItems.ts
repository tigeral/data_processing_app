export type DroppedItemType = "file" | "directory" | "url" | "web-image" | "unknown";

export interface DroppedItem {
  type: DroppedItemType;
  name: string;
  mime_type?: string;
  size?: number;
  url?: string;
  children?: string[];
}

function isUrl(value: string): boolean {
  try {
    const url = new URL(value.trim());
    return url.protocol === "http:" || url.protocol === "https:";
  } catch {
    return false;
  }
}

async function readDirectoryEntries(entry: FileSystemDirectoryEntry): Promise<string[]> {
  return new Promise((resolve) => {
    const reader = entry.createReader();
    reader.readEntries((entries) => {
      resolve(entries.map((e) => e.name));
    });
  });
}

async function processFileEntry(entry: FileSystemFileEntry): Promise<File> {
  return new Promise((resolve, reject) => entry.file(resolve, reject));
}

export async function detectDroppedItems(dt: DataTransfer): Promise<DroppedItem[]> {
  const results: DroppedItem[] = [];

  // Prefer DataTransferItemList when available (gives us directory access)
  if (dt.items && dt.items.length > 0) {
    const itemPromises: Promise<DroppedItem | null>[] = [];

    for (const item of Array.from(dt.items)) {
      if (item.kind === "string") {
        itemPromises.push(
          new Promise((resolve) => {
            item.getAsString((value) => {
              const trimmed = value.trim();
              if (!trimmed) {
                resolve(null);
                return;
              }
              if (isUrl(trimmed)) {
                // Distinguish a plain URL from a web image drop:
                // a web image drag from a browser page sets type to "text/uri-list"
                // but also carries an image/* type in some browsers. We treat
                // text/uri-list string items pointing to image paths as web-image.
                const looksLikeImage = /\.(png|jpe?g|gif|webp|svg|bmp|ico)(\?.*)?$/i.test(trimmed);
                resolve({
                  type: looksLikeImage ? "web-image" : "url",
                  name: trimmed,
                  url: trimmed,
                });
              } else {
                resolve({ type: "unknown", name: trimmed });
              }
            });
          })
        );
      } else if (item.kind === "file") {
        const entry = item.webkitGetAsEntry?.();
        if (entry?.isDirectory) {
          itemPromises.push(
            (async () => {
              const children = await readDirectoryEntries(entry as FileSystemDirectoryEntry);
              return {
                type: "directory" as DroppedItemType,
                name: entry.name,
                children,
              };
            })()
          );
        } else if (entry?.isFile) {
          itemPromises.push(
            (async () => {
              const file = await processFileEntry(entry as FileSystemFileEntry);
              return {
                type: "file" as DroppedItemType,
                name: file.name,
                mime_type: file.type || undefined,
                size: file.size,
              };
            })()
          );
        } else {
          // Fallback via File object (no entry API)
          const file = item.getAsFile();
          if (file) {
            results.push({
              type: "file",
              name: file.name,
              mime_type: file.type || undefined,
              size: file.size,
            });
          }
          itemPromises.push(Promise.resolve(null));
        }
      }
    }

    const resolved = await Promise.all(itemPromises);
    for (const item of resolved) {
      if (item) results.push(item);
    }
  } else if (dt.files.length > 0) {
    // Fallback for browsers without DataTransferItemList
    for (const file of Array.from(dt.files)) {
      results.push({
        type: "file",
        name: file.name,
        mime_type: file.type || undefined,
        size: file.size,
      });
    }
  }

  return results;
}
