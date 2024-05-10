/**
 * React component for displaying predictions in a table format.
 * @param {Object} props - Props passed to the component.
 * @param {string} props.prediction - The prediction string to be displayed.
 * @returns {JSX.Element} JSX representation of the Prediction Table component.
 */
import React from 'react';

function PredictionTable({ prediction }) {
  /**
   * Function to split the prediction string into an array of individual predictions.
   * @param {string} prediction - The prediction string to be split.
   * @returns {Array<string>} An array of individual predictions.
   */
  const splitPredictions = (prediction) => {
    // Split the string using the regex that looks for numbers followed by a period and a space
    return prediction.split(/(\(.*?\))+/).filter(Boolean);
  };

  /**
   * Array containing individual predictions.
   * @type {Array<string>}
   */
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
                <td style={{textAlign: 'center'}}>{index + 1}</td>
                <td style={{textAlign: 'center'}}>{item}</td>
            </tr>
          );} return null;})}
        </tbody>
      </table>
    </div>
  );
}

export default PredictionTable;
