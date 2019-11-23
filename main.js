var box_id;
var authenticated = false;
const proxy= "https://cors-anywhere.herokuapp.com/";
const mainurl = "https://t8al0f4vqf.execute-api.us-east-2.amazonaws.com/secureBox-api/";

// onload functions
window.onload = function() {
    var btn = document.getElementById("authenticateButton");
    btn.onclick = authenticate;
}

window.onload = function() {
    var btn = document.getElementById("registerButton2");
    btn.onclick = register;
}

window.onload = function() {
    var btn = document.getElementById("addOrderButton");
    btn.onclick = addOrder;
}

window.onload = function() {
    var btn = document.getElementById("viewOrdersButton");
    btn.onclick = viewOrders;
}

window.onload = function() {
    var btn = document.getElementById("getLockStatusButton");
    btn.onclick = getLockStatus;
}

window.onload = function() {
    var btn = document.getElementById("setAccessCodeButton");
    btn.onclick = setAccessCode;
}

// REST API requests
function authenticate() {
    box_id=document.getElementById("boxID").value;
    var accessCode=document.getElementById("access_code").value;
    var url1 = proxy+mainurl+'authenticate';
    var url2 = proxy+mainurl+'getUsername';
    const data = {'box_id': box_id, 'code': String(accessCode)}
    const stringData = JSON.stringify(data);
    const xhr = new XMLHttpRequest();
    const xhr2 = new XMLHttpRequest();
    xhr.open('POST', url1);
    xhr2.open('POST', url2);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr2.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var obj = JSON.parse(xhr.responseText);
                authenticated = obj.Open;
                if (authenticated) {
                    document.getElementById("authenticated").innerHTML = 'success!'.fontcolor('green');
                    document.getElementById("header").innerHTML = 'My Box: ' + String(box_id);
                } else {
                    document.getElementById("authenticated").innerHTML = 'failure!'.fontcolor('red');
                    document.getElementById("header").innerHTML = 'My Box';
                }
            } else {
                alert(xhr.statusText);
            }
        }
    }
    xhr2.onload = function() {
        if (xhr2.readyState === 4) {
            if (xhr2.status === 200) {
                var obj = JSON.parse(xhr2.responseText);
                if (authenticated) {
                    document.getElementById("profileHeader").innerHTML = obj.username + '\'s Profile';
                } else {
                    document.getElementById("profileHeader").innerHTML = 'My Profile';
                }
            } else {
                alert(xhr.statusText);
            }
        }
    }
    xhr.send(stringData);
    xhr2.send(stringData);
    getPhoneNumber();
}  

function addOrder() {
    var tracking_id=document.getElementById("trackingID").value;
    if (authenticated) {
        var url=proxy+mainurl+'addOrder';
        const data = {'box_id': box_id, 'tracking_id': tracking_id}
        const stringData = JSON.stringify(data);
        const xhr = new XMLHttpRequest();
        xhr.open('POST', url);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(stringData);
        document.getElementById("needAccess").innerHTML = 'added!'.fontcolor('green');
    } else {
        document.getElementById("needAccess").innerHTML = 'must authenticate first.'.fontcolor('red');
    }
}  

function viewOrders() {
    if (authenticated) {
        var url = proxy+mainurl+'viewOrders';
        const data = {'box_id': box_id}
        const stringData = JSON.stringify(data);
        const xhr = new XMLHttpRequest();
        xhr.open('POST', url);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onload = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    var obj = JSON.parse(xhr.responseText);
                    document.getElementById("orders").innerHTML = obj.Orders;
                } else {
                    alert(xhr.statusText);
                }
            }
        }
        xhr.send(stringData);
    } else {
        document.getElementById("orders").innerHTML = 'must authenticate first.'.fontcolor('red');
    }
}  

function getLockStatus() {
    if (authenticated) {
        var url=proxy+mainurl+'getLockStatus';
        const data = {'box_id': box_id}
        const stringData = JSON.stringify(data);
        const xhr = new XMLHttpRequest();
        xhr.open('POST', url);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onload = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    var obj = JSON.parse(xhr.responseText);
                    if (obj.locked === true)
                        document.getElementById("boxStatus").innerHTML = 'locked';
                    else
                        document.getElementById("boxStatus").innerHTML = 'unlocked';
                } else {
                    alert(xhr.statusText);
                }
            }
        }
        xhr.send(stringData);
    } else {
        document.getElementById("boxStatus").innerHTML = 'must authenticate first.'.fontcolor('red');
    }
}  

function setAccessCode() {
    if (authenticated) {
        document.getElementById("needAccess1").innerHTML = '';
        var access_code=document.getElementById("accessCode").value;
        var url = proxy+mainurl+'setAccessCode'
        const data = {'box_id': box_id, 'access_code': String(access_code)}
        const stringData = JSON.stringify(data);
        const xhr = new XMLHttpRequest();
        xhr.open('POST', url);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(stringData);
        document.getElementById("needAccess1").innerHTML = 'success!'.fontcolor('green');
    } else {
        document.getElementById("needAccess1").innerHTML = 'must authenticate first.'.fontcolor('red');
    }
}  

function getPhoneNumber() {
    if (authenticated) {
        var url=proxy+mainurl+'getPhoneNumber';
        const data = {'box_id': box_id}
        const stringData = JSON.stringify(data);
        const xhr = new XMLHttpRequest();
        xhr.open('POST', url);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onload = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    var obj = JSON.parse(xhr.responseText);
                    document.getElementById("phoneNum").innerHTML = 'Phone Number: ' + obj.phone_number;
                } else {
                    alert(xhr.statusText);
                }
            }
        }
        xhr.send(stringData);
    }
}

function register() {
    box_id=document.getElementById("box_id").value;
    var access_code=document.getElementById("access_code").value;
    var phone_number=document.getElementById("phoneNumber").value;
    var username=document.getElementById("userName").value;
    var url=proxy+mainurl+'register';
    const data = {'box_id': box_id, 'access_code': String(access_code), 'phone_number': String(phone_number), 'username': String(username)}
    const stringData = JSON.stringify(data);
    console.log(stringData);
    const xhr = new XMLHttpRequest();
    xhr.open('POST', url);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var obj = JSON.parse(xhr.responseText);
                if (obj.Registered === true) {
                    document.getElementById("result").innerHTML = 'success!'.fontcolor('green');
                } else {
                    document.getElementById("result").innerHTML = 'an account for this box ID already exists'.fontcolor('red');
                }
            } else {
                alert(xhr.statusText);
            }
        }
    }
    xhr.send(stringData);
}

