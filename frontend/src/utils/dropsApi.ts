import type { DroppedItem } from "./detectDroppedItems";

const BASE_URL = "http://localhost:8000";

export async function sendDrops(items: DroppedItem[]): Promise<void> {
  const response = await fetch(`${BASE_URL}/api/v1/drops`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ items }),
  });
  if (!response.ok) {
    throw new Error(`Server responded with ${response.status}`);
  }
}
