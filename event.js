var event = require('events');
const { emit } = require('process');

var eventEmitter = new event.EventEmitter();

var connectionHandle = function (data){
    console.log('connection successful' + data);
}
eventEmitter.on('connection', connectionHandle);

eventEmitter.emit('connection', new Date());