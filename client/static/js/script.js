const apiBase = 'https://aircon.iot.elf.moe/api/v1';
var username = null;
var token = null;
var mode = null;
var value = null;

function endpoint(uri) {
    return apiBase + uri;
}

function getApiJson(uri) {
    return fetch(uri, {mode: 'cors'}).then(data => {
        return data.json();
    });
}

function postApiJson(uri, body) {
    return fetch(uri, {
        method: 'POST',
        mode: 'cors',
        body: body,
    }).then(data => {
        return data.json();
    });
}

var $ = riot.observable();
riot.compile(() => {
    riot.mount('current-temp');

    if(localStorage.username === undefined || localStorage.token === undefined) {
        riot.mount('login-form');
    } else {
        getApiJson(endpoint(`/check?username=${localStorage.username}&token=${localStorage.token}`)).then(data => {
            if(data.result) {
                username = localStorage.username;
                token = localStorage.token;
                riot.mount('aircon-control');
            } else {
                riot.mount('login-form');
            }
        });
    }

    getApiJson(endpoint('/state')).then(data => {
        mode = data.mode;
        value = data.value;
        $.trigger('stateChanged');
    });
});
