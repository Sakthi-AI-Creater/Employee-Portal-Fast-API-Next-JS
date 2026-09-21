"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";

export default function Home() {
  const [status, setStatus] = useState("Checking backend...");

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const response = await api.get("/health");

        setStatus(response.data.status);
      } catch (error) {
        setStatus("Backend unavailable");
      }
    };

    checkBackend();
  }, []);

  return (
    <main className="flex min-h-screen items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold">
          Employee Portal
        </h1>

        <p className="mt-4">
          Backend status:
          {" "}
          <span className="font-semibold">
            {status}
          </span>
        </p>
      </div>
    </main>
  );
}