import { API_BASE, getThreadID } from "./config.js";
import { addMessage, createBotMessage } from "./ui.js";

export async function sendMessage(){

    const input = document.getElementById("message");

    const msg = input.value.trim();

    if(msg === "") return;

    addMessage("user", msg);

    input.value = "";

    const botDiv = createBotMessage();

    try{

        const response = await fetch(`${API_BASE}/chat-stream`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: msg,
                thread_id: getThreadID()
            })

        });

        const reader = response.body.getReader();

        const decoder = new TextDecoder();

        while(true){

            const { done, value } = await reader.read();

            if(done) break;

            botDiv.innerText += decoder.decode(value);

        }

    }
    catch(error){

        botDiv.innerText = "Error connecting to server";

        console.error(error);

    }

}
