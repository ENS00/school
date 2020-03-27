"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
/*
** Lorenzo Tomasello
** 27/03/2020
** Introduction to templates rendering plugin
*/
const fastify = require("fastify");
const staticFile = require("fastify-static");
const pointOfView = require("point-of-view");
const path = require("path");
var app = fastify({ logger: true });
class User {
    constructor(firstname, lastname) {
        this.firstname = firstname;
        this.lastname = lastname;
        this.list = [];
        this.id = User.getNewId();
    }
    static getNewId() {
        if (!this.latestId)
            this.latestId = 1;
        else
            this.latestId++;
        return this.latestId;
    }
}
// User list
let database = [
    new User('Paolo', 'Rossi'),
    new User('Silvana', 'Falchi')
];
// we provide a little description for every key, so we can visualize it better
let descriptions = {
    // notifications
    browser: 'Ricezione notifiche su Browser',
    email: 'Ricezione notifiche via Email',
    sms: 'Ricezione notifiche via SMS'
};
// On first opening choose the first user in the list to log in
let selectedUser = 0;
app.register(pointOfView, {
    engine: {
        ejs: require('ejs')
    }
});
// tool to get form data in request.body
app.register(require('fastify-formbody'));
// styles folder contains static files
app.register((instance, opts, next) => {
    instance.register(staticFile, {
        root: path.join(__dirname, 'css'),
        prefix: '/css/'
    });
    next();
});
app.get('/', (req, reply) => {
    reply.view('/templates/index.ejs', {
        currentUser: database[selectedUser],
        data: {
            list: database,
            descriptions
        }
    });
});
app.get('/switchuser/:id', (req, reply) => {
    let id = Number(req.params.id);
    let switchuser = database.findIndex((user) => user.id === id);
    if (switchuser != -1) {
        selectedUser = switchuser;
        reply.redirect('/');
    }
    else
        reply.view('/templates/error.ejs', {
            currentUser: database[selectedUser],
            data: {
                error: true,
                message: 'Utente non trovato!'
            }
        });
});
app.get('/form', (req, reply) => {
    reply.view('/templates/form.ejs', {
        currentUser: database[selectedUser],
        edit: 'update'
    });
});
app.get('/insert', (req, reply) => {
    reply.view('/templates/form.ejs', {
        currentUser: database[selectedUser],
        edit: 'insert'
    });
});
app.get('/items/:id', (req, reply) => {
    let id = req.query.id;
    reply.view('/templates/details.ejs', {
        currentUser: database[selectedUser],
        data: {
            id: id,
            title: 'elemento con id ' + id
        }
    });
});
app.post('/update', (req, reply) => {
    let returnObj = {
        error: false,
        message: ''
    };
    if (req.body.edit == 'update') {
        try {
            database[selectedUser].firstname = req.body.firstname;
            database[selectedUser].lastname = req.body.lastname;
            database[selectedUser].list = [];
            if (req.body.list_email)
                database[selectedUser].list.push('email');
            if (req.body.list_sms)
                database[selectedUser].list.push('sms');
            if (req.body.list_browser)
                database[selectedUser].list.push('browser');
        }
        catch (e) {
            returnObj.error = true;
            returnObj.message = e.name + ':' + e.message;
        }
    }
    else if (req.body.edit == 'insert') {
        try {
            let newUser = new User(req.body.firstname, req.body.lastname);
            if (req.body.list_email)
                newUser.list.push('email');
            if (req.body.list_sms)
                newUser.list.push('sms');
            if (req.body.list_browser)
                newUser.list.push('browser');
            database.push(newUser);
        }
        catch (e) {
            returnObj.error = true;
            returnObj.message = e.name + ':' + e.message;
        }
    }
    else
        returnObj.error = true;
    reply.view('/templates/update.ejs', {
        currentUser: database[selectedUser],
        data: returnObj
    });
});
app.listen(3000, (err, address) => {
    if (err)
        throw err;
    app.log.info(`server listening on ${address}`);
});
