async function analyzeLog(){

    const log=document.getElementById("logInput").value;

    const result=document.getElementById("result");

    const loading=document.getElementById("loading");

    result.innerHTML="";

    loading.style.display="block";

    try{

        const response=await fetch("/analyze",{

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },

            body:JSON.stringify({

                log:log

            })

        });

        const data=await response.json();

        loading.style.display="none";
        
        if (data.status === "error"){
        
            result.innerHTML=
            "<h3> " + data.message + "</h3>";
        } else {
        
            result.innerHTML=
            "<pre>"+
            JSON.stringify(data,null,4)+
            "</pre>";
        }

    }

    catch(error){

        loading.style.display="none";

        result.innerHTML=

            "<b>Error:</b> "+

            error;

    }

}