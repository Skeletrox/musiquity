import axios from 'axios';


let getUserData = (user, cb) => {
    axios.get(`https://localhost:8000/data/get_tracks/${user}`).then(response => {
        let res = response.data;
        let returnable = res.returnable;
        cb(returnable);
    }).catch(err => {
        cb(null, err);
    });
}

let getUserCutoffData = (user, cb) => {
    axios.get(`https://localhost:8000/data/get_cutoffs/${user}`).then(response => {
        let res = response.data;
        let returnable = res.cutoffs;
        cb(returnable);
    }).catch(err => {
        cb(null, err);
    });
}

let getUserMetrics = (user, cb) => {
    axios.get(`https://127.0.0.1:8000/data/read/${user}/10m`).then(response => {
        let res = response.data;
        let resp = res.points;
        let returnable = [];
        for (let r in resp) {
            returnable.push({x: r, y: resp[r].heart_rate});
        }
        console.log(returnable)
        cb(returnable, null);
    }).catch(err => {
        cb(null, err);
    });
}

export { getUserData, getUserCutoffData, getUserMetrics };