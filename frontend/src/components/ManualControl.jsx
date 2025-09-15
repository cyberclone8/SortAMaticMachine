import React, { useRef, useState, useEffect } from "react";
import { Joystick } from "lucide-react";
import Swal from "sweetalert2"
import { createSocket } from "../utils/createSocket";

const ManualControl = () => {
    const [servo1, setServo1] = useState(true);
    const [servo2, setServo2] = useState(true);
    const [servo3, setServo3] = useState(true);
    const [servo4, setServo4] = useState(true);
    const valueText = useRef(null);

    const [running, setRunning] = useState(false);


    const handleToggle = async () => {
        const action = running ? "start" : "stop";
        const url = `http://localhost:8000/conveyor/${action}`;

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
            });

            const data = await response.json();
            console.log(`Server response:`, data);

            setRunning(!running); // toggle button state only if request succeeds
        } catch (error) {
            console.error("Error sending request:", error);
        }
    };

    // Servo click logic
    const handleServoClick = (servo) => {
        if (servo === 1) {
            setServo1(false);
            setServo2(true);
        } else if (servo === 2) {
            if (!servo1) {
                setServo1(true);
                setServo2(false);
            } else {
                setServo2(false);
                setServo1(true);
            }
        } else if (servo === 3) {
            if (!servo1) {
                setServo1(false);
                setServo2(false);
            }
            setServo3(false);
            setServo4(true);
        } else if (servo === 4) {
            if (!servo3) {
                setServo3(true);
                setServo4(false);
            } else {
                setServo4(false);
                setServo3(true);
            }
        }
    };

    const handleReset = () => {
        Swal.fire({
            title: "Are you sure?",
            text: "You won't be able to revert this!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Yes, reset it!"
        }).then((result) => {
            if (result.isConfirmed) {
                setServo1(true);
                setServo2(true);
                setServo3(true);
                setServo4(true);
            }
        });
    };

    const getButtonClass = (enabled) =>
        `btn btn-primary btn-soft w-full h-full rounded-lg shadow-sm ${!enabled ? "btn-disabled opacity-50" : ""
        }`;

    return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="w-full max-w-3xl bg-white shadow-sm rounded-2xl overflow-hidden">
                {/* Header */}
                <div className="flex p-4 gap-2">
                    <Joystick />
                    <h2 className="text-2xl font-bold">Manual Control</h2>
                </div>
                <hr />

                {/* Servo Header */}
                <div className="flex items-center justify-between p-2 bg-base-200">
                    <h3 className="text-lg font-bold">Servo Control</h3>
                    <button className="text-lg font-bold btn btn-soft btn-error rounded-sm"
                        onClick={handleReset}
                    >Reset</button>
                </div>

                {/* Servo Container */}
                <div className="h-[200px]">
                    <div className="h-[200px] grid grid-cols-4 p-2 gap-4">
                        <button
                            className={getButtonClass(servo1)}
                            onClick={() => handleServoClick(1)}
                            disabled={!servo1}
                        >
                            <span className="text-lg">Servo 1</span>
                        </button>
                        <button
                            className={getButtonClass(servo2)}
                            onClick={() => handleServoClick(2)}
                            disabled={!servo2}
                        >
                            <span className="text-lg">Servo 2</span>
                        </button>
                        <button
                            className={getButtonClass(servo3)}
                            onClick={() => handleServoClick(3)}
                            disabled={!servo3}
                        >
                            <span className="text-lg">Servo 3</span>
                        </button>
                        <button
                            className={getButtonClass(servo4)}
                            onClick={() => handleServoClick(4)}
                            disabled={!servo4}
                        >
                            <span className="text-lg">Servo 4</span>
                        </button>
                    </div>
                </div>

                {/* Conveyor Header */}
                <div className="flex items-center justify-start p-2 bg-base-200">
                    <h3 className="text-lg font-bold">Conveyor Control</h3>
                </div>

                {/* Conveyor Body */}
                <div className="h-[200px] flex items-center justify-center">
                    <div
                        onClick={handleToggle}
                        className={`w-[300px] h-[180px] btn rounded-lg shadow-md p-2 flex items-center justify-center cursor-pointer
                        ${running ? "btn-accent" : "btn-error"}`}
                    >
                        <span className="font-bold text-3xl getText" ref={valueText}>{running ? "START" : "STOP"}</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ManualControl;