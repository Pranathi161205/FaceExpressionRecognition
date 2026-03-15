import React, {useState} from "react";
import {useDropzone} from "react-dropzone";
import axios from "axios";

function ImageEmotion() {

const [emotion,setEmotion] = useState("");

const onDrop = async (acceptedFiles) => {

const file = acceptedFiles[0];

const reader = new FileReader();

reader.onload = async () => {

const base64 = reader.result;

const res = await axios.post("http://localhost:5000/detect",{
image: base64
});

setEmotion(res.data.emotion);

};

reader.readAsDataURL(file);
};

const {getRootProps,getInputProps} = useDropzone({onDrop});

return (

<div>

<div {...getRootProps()} style={{
border:"2px dashed gray",
padding:"40px",
textAlign:"center"
}}>

<input {...getInputProps()} />

<p>Drag & Drop Image Here</p>

</div>

<h2>{emotion}</h2>

</div>
);
}

export default ImageEmotion;