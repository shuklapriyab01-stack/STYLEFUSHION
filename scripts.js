async function getRecommendation(){

let gender=document.getElementById("gender").value
let occasion=document.getElementById("occasion").value
let season=document.getElementById("season").value

try{

let response=await fetch("http://127.0.0.1:5000/recommend",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

gender:gender,
occasion:occasion,
season:season

})

})

let data=await response.json()

document.getElementById("output").innerText=
"Recommended Outfit: "+data.recommendation

}

catch(error){

document.getElementById("output").innerText=
"Error connecting to server"

}

}