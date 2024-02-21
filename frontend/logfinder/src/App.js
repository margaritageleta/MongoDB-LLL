
import { Button } from '@mui/material';
import './App.css';
import axios from 'axios';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { useState } from 'react';

function App() {
  const[userInput, setUserInput] = useState('');
  const[aiResponse, setAiResponse] = useState('');

  function handleInput(event) {
    setUserInput(event.target.value);
  }

  const handleSubmit = (event) => {
    event.preventDefault();

    axios.get(`http://localhost:8000/vector_search?query=${userInput}`)
    .then((res) => {
      var loglines = res.data.map(item => item.logline);
      setAiResponse(loglines);
    })
  } 

  function generateHTMLList(logLines) {
    const listItems = logLines.map(line => `<p>${line}</p>`);
    const html = `<ul>${listItems.join('')}</ul>`;
    return html;
  }

  return (
    <div className="App">
        <h1 className="App-title">Live Laugh Log</h1>
        <Button variant="contained" component="label">
            Upload File
              <input
                type="file"
                hidden
              />
        </Button>
        <br></br>
        <Box>
      <TextField id="outlined-basic" 
      size='large' 
      label="What are you searching for?" 
      variant="outlined" 
      sx={{ width: '80%' }} 
      value={userInput}
      onChange={handleInput}/> 
      <Button variant="contained"  style={{height: '55px'}} color="primary" type='submit' onClick={handleSubmit}>Submit</Button>
      </Box>
      {aiResponse ? <div dangerouslySetInnerHTML={{ __html: generateHTMLList(aiResponse) }} /> : null}
    </div>
  );
}

export default App;
