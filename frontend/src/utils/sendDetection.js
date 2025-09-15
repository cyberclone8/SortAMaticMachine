export async function sendDetection(detection) {
  try {
    const response = await fetch("http://localhost:8000/segregate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(detection),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data; // this can be awaited in other files
  } catch (err) {
    console.error("Failed to send detection:", err);
    throw err;
  }
}