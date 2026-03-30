 document.getElementById("verifyForm").onsubmit = async function(event) {
            event.preventDefault();

            const formData = new FormData();
            formData.append("file1", document.getElementById("file1").files[0]);
            formData.append("file2", document.getElementById("file2").files[0]);

            try {
                const response = await fetch("/verify", {
                    method: "POST",
                    body: formData
                });

                const result = await response.json();
                const resultDiv = document.getElementById("result");

                // Clear previous result
                resultDiv.innerHTML = "";

                // Create main message
                const message = document.createElement("div");
                message.className = result.message.includes("Same") ? "same" : "different";
                message.textContent = result.message;

                // Create similarity score
                const similarity = document.createElement("div");
                similarity.className = "similarity";
                if (result.similarity !== undefined) {
                    similarity.textContent = "Similarity score: " + result.similarity.toFixed(2);
                }

                resultDiv.appendChild(message);
                resultDiv.appendChild(similarity);

            } catch (error) {
                console.error("Error:", error);
                document.getElementById("result").innerHTML = "<div class='different'>Request failed.</div>";
            }
        };

         async function countVisit() {
            const response = await fetch("/visit", { method: "POST" });
            const data = await response.json();
            document.getElementById("counter").innerText =
                "Unique visitors: " + data.unique_visitors;
        }
