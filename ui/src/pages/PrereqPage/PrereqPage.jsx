/**
 * React component for the Prerequisite Page.
 * This component displays a graph of course prerequisites using Cytoscape.
 * @component
 */
import TopBar from "../../components/TopBar/TopBar";
import CytoscapeComponent from 'react-cytoscapejs';
import dagre from 'cytoscape-dagre';
import { courseData } from "../../components/CourseList/courseData";
import cytoscape from "cytoscape";

/**
 * Function to retrieve course data from courseData object.
 * @returns {Array<Object>} Array containing course data objects.
 */
function getCourseData() {
  const arr = [];
  for (const key in courseData) {
    const id = key.match(/\b[A-Z]{1,4} \d{4}\b/g)[0];
    const postreqs = [];
    for (const postreqKey in courseData) {
      if (courseData[postreqKey].prereq.includes(id)) {
        postreqs.push(postreqKey.match(/\b[A-Z]{1,4} \d{4}\b/g)[0]);
      }
    }
    arr.push({
      id: id.replace(" ", ""),
      name: key,
      desc: courseData[key].desc[courseData[key].desc.length - 1],
      prereq:
        courseData[key].prereq.map(pr => pr.replace(" ", "")),
      postreq: postreqs.map(pr => pr.replace(" ", "")),
    });
  }

  return arr;
}

/**
 * Function to create an edge between two nodes.
 * @param {string} sourceId - ID of the source node.
 * @param {string} targetId - ID of the target node.
 * @param {Array<Object>} nodes - Array of node objects.
 * @param {Array<Object>} edges - Array of edge objects.
 * @returns {Object|null} Edge object if creation is successful, otherwise null.
 */
function createEdge(sourceId, targetId, nodes, edges) {
  if (nodes.some(n => n.data.id === sourceId)
    && nodes.some(n => n.data.id === targetId)
    && edges.every(e => e.data.label !== `${sourceId} -> ${targetId}`)) {
    return {
      data: {
        source: sourceId,
        target: targetId,
        label: `${sourceId} -> ${targetId}`,
      },
    };
  } else {
    return null;
  }
}

/**
 * Functional component representing the Prerequisite Page.
 * @returns {JSX.Element} JSX representation of the Prerequisite Page.
 */
function PrereqPage() {
  cytoscape.use(dagre);

  /**
   * Event handler for interactions with the Cytoscape component.
   * @param {Object} cy - Cytoscape instance.
   */
  function onCyInteraction(cy) {
    // Uncomment if more work with cytoscape is done in the future
    // const myCyRef = cy;

    // console.log("EVT", cy);

    // cy.on("tap", "node", evt => {
    //   var node = evt.target;
    //   console.log("EVT", evt);
    //   console.log("TARGET", node.data());
    //   console.log("TARGET TYPE", typeof node[0]);
    // });
  }

  const courses = getCourseData();
  const data = { nodes: [], edges: [] };
  for (const course of courses) {
    if (course.prereq.every(p => !p.startsWith('CSCI')) && course.postreq.every(p => !p.startsWith('CSCI'))) { continue; }
    data.nodes.push({
      data: {
        id: `${course.id}`,
        label: `${course.name}`,
        type: 'course',
      },
    });
    for (const prereq of course.prereq) {
      const e = createEdge(prereq, course.id, data.nodes, data.edges);
      if (e) {
        data.edges.push(e);
      }
    }
    for (const postreq of course.postreq) {
      const e = createEdge(course.id, postreq, data.nodes, data.edges);
      if (e) {
        data.edges.push(e);
      }
    }
  }

  const layout = {
    name: "dagre",
    fit: true,
    circle: true,
    directed: true,
    padding: 50,
    spacingFactor: 2,
    animate: true,
    animationDuration: 250,
    avoidOverlap: true,
    nodeDimensionsIncludeLabels: false
  };

  const cytoscapeStyles = [
    {
      selector: "node",
      style: {
        backgroundColor: "#4a56a6",
        width: 30,
        height: 30,
        label: "data(label)",
        "text-wrap": 'wrap',
        "text-max-width": '200px',
        // "width": "mapData(score, 0, 0.006769776522008331, 20, 60)",
        // "height": "mapData(score, 0, 0.006769776522008331, 20, 60)",
        // "text-valign": "center",
        // "text-halign": "center",
        "overlay-padding": "6px",
        "z-index": "10",
        //text props
        "text-outline-color": "#4a56a6",
        "text-outline-width": "2px",
        color: "#AAD8FF",
        fontSize: 20
      }
    },
    {
      selector: "node:selected",
      style: {
        "border-width": "6px",
        "border-color": "#AAD8FF",
        "border-opacity": "0.5",
        "background-color": "#77828C",
        width: 50,
        height: 50,
        //text props
        "text-outline-color": "#77828C",
        "text-outline-width": 8
      }
    },
    {
      selector: "node[type='device']",
      style: {
        shape: "rectangle"
      }
    },
    {
      selector: "edge",
      style: {
        width: 3,
        // "line-color": "#6774cb",
        "line-color": "#000000",
        "target-arrow-color": "#000000",
        "target-arrow-shape": "triangle",
        "curve-style": "bezier"
      }
    }
  ];

  return (
    <div>
      <TopBar></TopBar>
      <div style={{ border: "1px solid", backgroundColor: "#ffffff" }}>
        <CytoscapeComponent
          elements={CytoscapeComponent.normalizeElements(data)}
          style={{ width: '100%', height: '957px' }}
          zoomingEnabled={true}
          maxZoom={5}
          minZoom={0.3}
          boxSelectionEnabled={true}
          layout={layout}
          stylesheet={cytoscapeStyles}
          cy={onCyInteraction}
        ></CytoscapeComponent>
      </div>
    </div>
  );
}

export default PrereqPage;
