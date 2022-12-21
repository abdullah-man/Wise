const myMap = L.map('map').setView([22.9074872, 79.07306671], 5);
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>';
// configuring tiles and adding them tiles to the map
const tileLayer = L.tileLayer(tileUrl, { attribution });
tileLayer.addTo(myMap);


// making a layer group to hold posts an another to hold markers
// as we want to clear the contents of these groups on each post click
var postLayerGroup = new L.LayerGroup();
var markerLayerGroup = new L.LayerGroup();


// marker for post is being set to appear as as green cloroed icon
var postMarkerIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

// first time click
var firstTimePostClick = new Boolean(false);
var firstTimeFilterGenerated = new Boolean(false);
// global var to hold complete data of  clicked post
var featureCollectionForFilter;
var filter_list = ["Alligator", "Longitudinal", "Lateral", "Pothole"];



// Now calling this function
for (let i = 0; i < storeList.length; i++) {
    // getting each featureCollection from the list of list: storeList
    var featureCollection = storeList[i];
    featureCollection = featureCollection[0]; // now it is a valid JSON object otherwise it appears to be an array

    featuresInFeatureCollection = featureCollection.features // this data is a list of features where first feature is of LineString type and rest are of Point type

    console.log("sending this data to generateList");
    console.log(featuresInFeatureCollection);
    // passing this list to generate the data
    generateList(featuresInFeatureCollection);

};



function onFilterToggle(nameOfFilter) {
    //check if a post is clicked already - if not do nothing
    if (firstTimePostClick == false) {
        // In this case reset the toggle to checked
        document.getElementById(nameOfFilter).checked = true;
        alert("Please first select the survey!");
    } else {
        // checking if the filter is to be inserted or deleted from filter_state
        if (filter_list.includes(nameOfFilter)) {
            // remove the name and generate the markers
            for (let i = 0; i < filter_list.length; i++) {
                // iterating over the list and checking where the filter name is present, then deleting it
                if (filter_list[i] == nameOfFilter) {
                    filter_list.splice(i, 1);
                }
            }
            console.log("after removal the list contains:     " + String(filter_list));
            // now generating the markers on the newly set filter criteria
            generateMarkers(featureCollectionForFilter);
        } else {
            // add the name and generate the markers
            filter_list.push(nameOfFilter);
            generateMarkers(featureCollectionForFilter);
            console.log("after addition the list contains:     " + String(filter_list));
        }
    }
}

function isInFilterList(damageClassData) {
    // a list of class names is passed to this function
    // if any one item from the passed list is present in the filter_list then it returns a yes
    for (let i = 0; i < damageClassData.length; i++) {
        // if filter list contains a member from damageClassData then return True else return False
        if (filter_list.includes(damageClassData[i])) {
            return true;
        }
    }
    return false;
}


function generateList(featureCollection) {
    const ul = document.querySelector('.postlist');
    // iterates over the list storeList in stores.js file
    // on each iteration each object (which is a survey) and add each as a list item in the index.html

    featureCollection.forEach((feature) => {

        if (feature.geometry.type == "LineString") {

            console.log("populating line strings in the list");

            // to create an element in JS
            const li = document.createElement('li');
            // then we want to add a div in this li element as we want to put some text and style it
            const div = document.createElement('div');
            // we also want to add a link to this element as we want to go to the marker on map when this li is clicked
            // so an anchor tag is needed to generate
            const a = document.createElement('a');
            // also we want to add a paragraph
            const p = document.createElement('p');


            // as we would like to add style info to the div, we need to give this div a class
            div.classList.add('shop-item');
            // as we want to add text to the link from name property of the geoJason object i.e. from stores.js file
            a.innerText = feature.properties.postTitile;
            // make the cursor a pointer when it hovers the link
            a.href = '#';
            // adding event listener to the 'a' so that flyToSurvey function may be called onclick
            a.addEventListener('click', () => { flyToSurvey(feature, featureCollection); });
            // we also need to add text to the paragraph
            p.innerText = feature.properties.desc;


            // Now we need to assemble all the things made up here
            // adding anchor tag and paragraph in the div
            div.appendChild(a);
            div.appendChild(p);
            // now we want to add this div to the li item
            li.appendChild(div);
            // finally we want to add this li item in the ul
            ul.appendChild(li);

            console.log("list generated successfully");

        };

    });

}


function generateMarkers(featureCollection) {
    // Emptying the ul that contains the markers data in order to avoid appending to the already populated markers
    var myUl = document.querySelector('.markerlist');
    myUl.innerHTML = '';

    // generating markers in the markers window
    const ul = document.querySelector('.markerlist');

    console.log(featureCollection);

    // generate the filter  -  it will be generated for once only although it is being called on each post and filter click
    generateFilter();

    featureCollection.forEach((feature) => {

        if (feature.geometry.type == "Point") {

            // Now getting the class data of this Point/Marker
            let classData = feature.properties.class;
            classData = classData.split(" ");
            console.log(classData);
            console.log("Extracted Class Data is: " + classData);

            // if any member of this classData is in the filter_list then the POINT gets displayed in the list otherwise it doesn't
            if (isInFilterList(classData)) {

                console.log("markers' list is being generated");

                // to create an element in JS
                const li = document.createElement('li');
                // then we want to add a div in this li element as we want to put some text and style it
                const div = document.createElement('div');
                // we also want to add a link to this element as we want to go to the marker on map when this li is clicked
                // so an anchor tag is needed to generate
                const a = document.createElement('a');
                // also we want to add a paragraph
                const p = document.createElement('p');

                // as we would like to add style info to the div, we need to give this div a class
                div.classList.add('marker-item');
                // as we want to add text to the link from name property of the geoJason object i.e. from stores.js file
                a.innerText = "marker";
                // make the cursor a pointer when it hovers the link
                a.href = '#';

                a.addEventListener('click', () => { showmarker(feature); });
                // we also need to add text to the paragraph
                p.innerText = feature.geometry.coordinates;

                // Now we need to assemble all the things made up here
                // adding anchor tag and paragraph in the div
                div.appendChild(a);
                div.appendChild(p);
                // now we want to add this div to the li item
                li.appendChild(div);
                // finally we want to add this li item in the ul
                ul.appendChild(li);



                console.log("marker list generated successfully");
            }

        };


    });



}


function generateFilter() {
    // generates filter html
    if (firstTimeFilterGenerated == false) {
        // if filter is generated already, do not recreate it. As on each generateMarkers, we'll be creating the filters
        // and this will make the handling of the filter state difficult
        const div = document.querySelector('#filter-list');
        const filterHtml = `
        <br>
        <p>Alligator Cracks:&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<label class="switch"><input type="checkbox" id="alligator" onchange="return onFilterToggle('Alligator')" checked> <span class="slider round"></span></label></p><br>
        <p>Longitudinal Cracks:&nbsp&nbsp&nbsp&nbsp&nbsp<label class="switch"><input type="checkbox" id="longitudinal" onchange="return onFilterToggle('Longitudinal')" checked> <span class="slider round"></span></label></p><br>
        <p>Lateral Cracks:&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<label class="switch"><input type="checkbox" id="lateral" onchange="return onFilterToggle('Lateral')" checked> <span class="slider round"></span></label></p><br>
        <p>Potholes:&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<label class="switch"><input type="checkbox" id="pothole" onchange="return onFilterToggle('Pothole')" checked> <span class="slider round"></span></label></p><br>
        <!-- button to generate report based off the selections made using filters -->
        <button class="button" onclick="generateReportPDF()" target="_blank">Generate Report</button>
        `;
        // adding the html to the selected div
        div.innerHTML = filterHtml;

        // set the boolean to True as the filter has been generated
        firstTimeFilterGenerated = true;
    } else {
        // if the filter is already generated then do nothing and return
        return;
    }
}


function makePopupContentMarker(feature) {
    // here we are going to generate an html markup to be shown in popup of a marker
    console.log(typeof(feature.properties.img))
    console.log(feature.properties.img)
    return ` 
        <div>
            <h4>Road Defect</h4>
            <p>Defect Details:</p>
            <p><b>Location:</b></p>
            <p>${feature.geometry.coordinates}</p>
            <p><b>Road Condition:</b></p>
            <img src="${feature.properties.img}" width="200" height="200" />
        </div>
     `;
}

function makePopupContentPost(feature) {
    // here we are going to generate an html markup to be shown in popup of a post
    return ` 
        <div>
            <h4>${feature.properties.postTitile}</h4>
            <p>Survey Details:</p>
            <p><b>Associated Plan:</b></p>
            <p>${feature.properties.postPlan}</p>
            <p><b>Description:</b></p>
            <p>${feature.properties.desc}</p>
        </div>
     `;
}


// A function to fly to the Surver point - The "feature" being passed to this function is 
async function flyToSurvey(feature, featureCollection) { // function is made async in order to use await as described below
    // feature:             The LinString Object. So that we fly to focus on this object.
    // featureCollection:   Complete list of features including LineString and Point types. 
    //                      So to pass to the generateMarkers function and save in global var of featureCollectionForFilter

    // For this function to work on-click, we need to add a 
    // event listener on the post which is being created dynamically
    // we'll add an event listener to the anchor 'a' where the list is being generated dynamically
    // a.addEventListener('click', () => { flyToSurvey(survey) });
    // Leaflet has aspecial function for flying called: flyTo. Its first argument is coordinates as in an array: []
    // store.geometry.coordinates gives a list so we have accessed its contents using index numbers
    // Point: flyTo requires longitude first then it asks for lattitude.


    // saving the complete data of the post (featureCollection) in a global variable in order to implement filter
    featureCollectionForFilter = featureCollection;
    //debugger;
    console.log(feature.geometry.coordinates)
    console.log("this is the feature as passed to flyToSurvey");
    console.log(feature);

    const lng = feature.geometry.coordinates[0][0];
    console.log("lng reading", lng);
    const lat = feature.geometry.coordinates[0][1];
    console.log("lat reading", lat);

    myMap.flyTo([lng, lat], 15); // 15 is the zoom level value
    // myMap.flyTo([lat, lng], 15);
    console.log("flying to the lat long");

    // On clicking the Post we also need to toggle a list of
    // markers associated with this post. Here we are generating this.

    generateMarkers(featureCollection);

    // send this feature collection to the global variable of : featureCollectionForFilter
    featureCollectionForFilter = featureCollection;
    console.log("feature collection for filter variable");
    console.log(featureCollectionForFilter);

    // wait for 2.5 seconds before executing next code - 
    // this is to avoid the creation of an overly large red line which fills the screen fully
    // when the code runs for the first time
    // in order to run this, we need to make the function async as await is available to async function only
    if (firstTimePostClick == false) {
        await new Promise(resolve => setTimeout(resolve, 2500));
        firstTimePostClick = true;
    } else if (myMap.getZoom() < 10) {
        // if zoom level is less than 10 then the we wait and clear the post layer group
        // if post layer group is not cleared, then there is bloating of red line from the last click
        // This else-if contains code to stop bloating of path line when a post is clicked and then user 
        // wants to zoom out and then click another post. In this case the last clicked post is still appearing before it 
        // gets cleared as being done by code in the following lines. The path line of the last clicked post gets bloated 
        // and covers the screen
        postLayerGroup.clearLayers();
        await new Promise(resolve => setTimeout(resolve, 2500));
    }



    // binding a popup to the post that contains details of the post
    postMarker = L.marker([lng, lat], { icon: postMarkerIcon });
    postMarker.bindPopup(makePopupContentPost(feature));

    // here we add this post-marker to postLayerGroup
    // but before adding thivar docDefinition = {s post, we clear the postLayerGroup so it may not contain any data from previous click on post
    // also we clear markerLayerGroup so that no markers are left on the map from previous post's markers' clicking
    postLayerGroup.clearLayers();
    markerLayerGroup.clearLayers();
    postLayerGroup.addLayer(postMarker);

    // Adding path line to the map
    const pathData = feature.geometry.coordinates; // reading the path data
    // using polyline to draw the path which is a list-of-list
    const pathLine = new L.Polyline(pathData, {
        color: 'red',
        weight: 3,
        opacity: 0.99,
        smoothFactor: 1
    });

    postLayerGroup.addLayer(pathLine);
    // Now adding this layer group to our map
    postLayerGroup.addTo(myMap);

}

function showmarker(feature) {
    // adds a marker to the map
    markerLayer = L.marker(feature.geometry.coordinates);
    markerLayer.bindPopup(makePopupContentMarker(feature));

    // here we add this marker to markerLayerGroup BUT before adding a new marker the previously added one gets deleted
    markerLayerGroup.clearLayers();
    markerLayerGroup.addLayer(markerLayer);
    // Now adding this marker layer group to our map
    markerLayerGroup.addTo(myMap);

}


function generateReportPDF() {
    // if a post is not clicked and report is being generated then do nothing
    // if (firstTimePostClick == false){
    //     alert("Please first select a survey to generate its report!");
    //     return;
    // }

    // getting the current post data to include general statistics in the report
    const currentPostData = featureCollectionForFilter;
    // getting filter state to filter this data on its basis and generate the report on the selected criteria
    const currentFilterState = filter_list;


    var pdfData = {
        content: [{
                text: 'Report',
                style: 'header'
            },
            'This is example text.',
            {
                text: 'Report',
                style: 'quote'
            },
            'This is also an example.',
        ],
        styles: {
            header: {
                fontSize: 16,
                bold: true,
                background: '#ff1'
            },
            subheader: {
                fontSize: 15,
                bold: true
            },
            quote: {
                italics: true
            },
            small: {
                fontSize: 8
            }
        }
    }

    // generating pdf
    pdfMake.createPdf(pdfData).download();
    // pdfMake.createPdf(pdfData).open({}, window); // opens in the same window

}