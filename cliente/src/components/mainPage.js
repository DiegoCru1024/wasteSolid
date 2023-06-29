import {useEffect, useRef, useState} from "react"
import axios from "axios"
import styles from '../css/mainStyle.module.css'

export default function MainPage() {
    const videoRef = useRef(null)
    const canvasRef = useRef(null)
    const mediaRecorderRef = useRef(null)
    const chunksRef = useRef([])
    const [response, setResponse] = useState({
        'cat': 'None',
        'pred': 'None'
    })
    const [isCapturing, setIsCapturing] = useState(false)
    const intervalIdRef = useRef(null)

    useEffect(() => {
        navigator.mediaDevices
            .getUserMedia({video: true})
            .then((stream) => {
                videoRef.current.srcObject = stream

                mediaRecorderRef.current = new MediaRecorder(stream)
                mediaRecorderRef.current.ondataavailable = handleDataAvailable
                mediaRecorderRef.current.start()
            })
            .catch((error) => {
                console.error("Error accessing camera:", error)
            })

        return () => {
            stopCapture() // Detiene la captura automática de frames al desmontar el componente
        }
    }, [])

    useEffect(() => {
        if (isCapturing) {
            startCapture()
        } else {
            stopCapture()
        }
    }, [isCapturing])

    const startCapture = () => {
        console.log("Iniciando captura...")
        intervalIdRef.current = setInterval(() => {
            const video = videoRef.current
            const canvas = canvasRef.current
            const context = canvas.getContext("2d")
            context.drawImage(video, 0, 0, canvas.width, canvas.height)

            canvas.toBlob((blob) => {
                sendFrame(blob)
            }, "image/jpeg", 1)
        }, 1000)
    }

    const stopCapture = () => {
        console.log("Deteniendo captura...")
        clearInterval(intervalIdRef.current)
        if (mediaRecorderRef.current) {
            mediaRecorderRef.current.stop()
        }
    }

    const handleDataAvailable = (event) => {
        if (event.data && event.data.size > 0) {
            chunksRef.current.push(event.data)
        }
    }

    const handleStartCapture = () => {
        setIsCapturing(true)
    }

    const handleStopCapture = () => {
        setIsCapturing(false)
    }

    const sendFrame = (blob) => {
        console.log("Enviando frame...")
        const formData = new FormData()
        formData.append("frame", blob, "frame.jpg")
        axios
            .post("http://localhost:5000/api/sendData", formData)
            .then((response) => {
                setResponse(response.data)
            })
            .catch((error) => {
                console.error("Error sending frame:", error)
            })
    }

    return (
        <div className={styles.mainContainer}>
            <div className={styles.imageContainer}>
                <video ref={videoRef} autoPlay muted/>
                <canvas ref={canvasRef}/>
            </div>
            <div>
                {isCapturing ? (
                    <button onClick={handleStopCapture}>Detener captura</button>
                ) : (
                    <button onClick={handleStartCapture}>Iniciar captura</button>
                )}
            </div>
            <div>
                <h2>Categoría: {response.cat}</h2>
                <h2>Predicción: {response.pred}</h2>
            </div>
        </div>
    )
}
