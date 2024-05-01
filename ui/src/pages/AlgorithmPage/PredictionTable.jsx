import React from 'react';

function PredictionTable({ prediction }) {
  // Function to split the prediction string into an array of individual predictions
  var int = 0;
  const splitPredictions = (prediction) => {
    // Split the string using the regex that looks for numbers followed by a period and a space
  return prediction.split(/(\(.*?\))+/).filter(Boolean);
  };

  const predictionsArray = splitPredictions(prediction);

  return (
    <div style={{display: 'flex', justifyContent: 'center'}}>
      <table style={{margin: 'auto'}}>
        <thead>
          <tr>
            <th>#</th>
            <th>Prediction</th>
          </tr>
        </thead>
        <tbody >
          {predictionsArray.map((item, index) => {
            if (item.trim() !== '') { return (
            <tr key={index}>
                <td style={{textAlign: 'center'}}>{++int}</td>
                <td style={{textAlign: 'center'}}>{item}</td>
            </tr>
          );} return null;})}
        </tbody>
      </table>
    </div>
  );
}

export default PredictionTable;