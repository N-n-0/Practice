const express = require('express');
const axios = require('axios');
const app = express();

const apiKey = '73ace1ac299469be6cc9d31d38d358e1';
const lat = '53.53'
const lon = '27.34'

const weatherApiUrl = `https://api.openweathermap.org/data/2.5/forecast?`;


app.get('/200', async (req, res) => {
  try {
    const response = await axios.get(`${weatherApiUrl}lat=${lat}&lon=${lon}&appid=${apiKey}`);
    res.status(response.status).send(response.data);
} catch (error) {
    res.status(error.response.status).send(error.response.data);
}
});


app.get('/304', async (req, res) => {
  try {
    const response = await axios.get(`${weatherApiUrl}lat=${lat}&lon=${lon}&appid=${apiKey}`,{
      headers: {
          'If-None-Match': '*'
      }
  } );
    res.status(response.status).send(response.data);
  } catch (error) {
    res.status(error.response.status).send(error.response.data);
}
});


app.get('/400', async (req, res) => {
    try {
      const response = await axios.get(`${weatherApiUrl}lon=${lon}&appid=${apiKey}`); 
      res.status(response.status).send(response.data);
  } catch (error) {
      res.status(error.response.status).send(error.response.data);
  }
  });


app.get('/401', async (req, res) => {
    try {
      const response = await axios.get(`${weatherApiUrl}lat=${lat}&lon=${lon}`);
        res.status(response.status).send(response.data);
    } catch (error) {
        res.status(error.response.status).send(error.response.data);
    }
    
});


app.get('/404', async (req, res) => {
   try {
      const response = await axios.get(`https://api.openweathermap.org/data/2/forecast?lat=${lat}&lon=${lon}&appid=${apiKey}`);
      res.status(response.status).send(response.data);
    } catch (error) {
     res.status(error.response.status).send(error.response.data);
    }
 });


app.get('/405', async (req, res) => {
   try {
     const response = await axios.patch(`${weatherApiUrl}lat=${lat}&lon=${lon}&appid=${apiKey}`);
     res.status(response.status).send(response.data);
   } catch (error) {
     res.status(error.response.status).send(error.response.data);
   }
});


app.get('/412', async (req, res) => {
   try {
     const response = await axios.get(`${weatherApiUrl}lat=${lat}&lon=${lon}&appid=${apiKey}`,{
       headers: {
           'If-Match': 'sometext'
       }
   } );
     res.status(response.status).send(response.data);
   } catch (error) {
     res.status(error.response.status).send(error.response.data);
   }
});


app.get('/413', async (req, res) => {
  try {
    const response = await axios.get(`${weatherApiUrl}lat=${lat}&lon=${lon}&appid=${apiKey}`,{
      headers: {
          'Content-Length': '1000000000'
      }
  } );
    res.status(response.status).send(response.data);
  } catch (error) {
    res.status(error.response.status).send(error.response.data);
}
});


app.get('/414', async (req, res) => {
  try {
    let points = '.'.repeat(10000000);
      const response = await axios.get(`${weatherApiUrl}lat=${lat}&lon=${lon}&appid=${apiKey}&p=${points}`);
      res.status(response.status).send(response.data);
  } catch (error) {
      res.status(error.response.status).send(error.response.data);
  }
});

app.listen(3333, () => {
    console.log('Application listening on port 3333!');
});
