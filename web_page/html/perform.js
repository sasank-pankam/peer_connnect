function initiate(code)
{   
    var connectToCode_;
    while(true)
    {
        try 
        {
            connectToCode_ = new WebSocket('ws://localhost:12345');
            break;
        }
        catch (error) 
        {
            console.error('::Connection error :', error);                                       //*debug
        }
    }
    console.log("connected to 12345");                                                              //*debug
    if (code == 1) 
        senderdetail = generateName(); 
    else  
        senderdetail = document.getElementById("user_name").value; 

    if (senderdetail == "")  return false;

    main_division.style.display = "flex";
    form_group.style.display = "none";
    display_name.textContent = senderdetail;
    connectToCode_.addEventListener('message', (event) => {

        if (event.data != "2ef7bde608ce5404e97d5f042f95f89f1c232871")
        {
            console.error('::Received unknown code handshake error :', event.data);
            return false;
        }
        else
            console.log('::Received message :', event.data);                                       //*debug
    });
    connectToCode_.addEventListener('open', (event) => {
        console.log("connected to python");                                                        //*debug
        connectToCode_.send("thisisausername_/!_"+senderdetail);
        console.log("Username sent")
    });
}


function sendmessages()                         
{
    const connecttocode_ = new WebSocket('ws://localhost:12345');
    if (focusedUser == null)
    {
        document.getElementById("intial_view").textContent="Select a user to chat";
        return false;
    }
    connecttocode_.addEventListener('open', (event) => {
        connecttocode_.send(createmessage());   
        console.log("message sent");                                                               //*debug
    });
    /*sending messages on port :12345 message syntax : "thisisamessage_/!_" + Content + "~^~" + focusedUser.id */
}


function recievedataFromPython()   
{
    var connectToCode_;
    try {
        connectToCode_ = new WebSocket('ws://localhost:12346');
    }
    catch (error) {
        console.error('::Connection error :', error);                                       //*debug
    }
    connectToCode_.addEventListener('open', (event) => {
        console.log("connected");                                                               //*debug
    });                                                                   
    connectToCode_.addEventListener('message', (event) => {
        var recievedata_ = event.data.split("_/!_");
        console.log('::Received message :'+recievedata_);                                       //*debug
        if (recievedata_[0] == "thisisamessage")
            recievedmessage(recievedata_[1]);

        else if (recievedata_[0] == "thisisausername")
            createtile(recievedata_[1]);

        else
            console.error('::Received unknown message :', event.data);                           //*debug
    });
    connectToCode_.addEventListener('close', (event) => {
        console.log('::Connection closed :', event.data);  
    });                                     
    /* data syntax : thisisamessage_/!_message~^~recieverid syntax of recieverid :
     name(^)ipaddress using port 12346 to recieve
       data syntax : thisisausername_/!_name(^)ipaddress
    */
}

// utitlities  : ---------------------------------------------------------------------------
focusedUser        =   document.getElementById(       ""      );
initial_view       =   document.getElementById( "intial_view" );
main_division      =   document.getElementById("main_division");
form_group         =   document.getElementById( "form_group"  );
display_name       =   document.getElementById( "display_name");
division_alive     =   document.getElementById( "alive_users" );
division_viewerpov =   document.getElementById(   "prattle"   );
let senderdetail   =   "";
let Spwaned   =   [];
let countMessage   =   {};
let users_list     =   {};


function generateName()
{
    var user_ = "random-"
    var possible_ = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for (var i = 0; i < 6; i++ )
    {
        user_ += possible_.charAt(Math.floor(Math.random() * possible_.length));
    }
    return user_;
}

function eventlisteners()
{
    document.getElementById("message").addEventListener("keyup", function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            document.getElementById("senderbutton").click();
        }
    });
}

function createtile(idin='') // idin is the id of the user to be added syntax : name(^)ipaddress
{
    var idin_=idin.split("(^)");
    document.getElementById("intial_view").textContent = "Click on Name to view chat";
    document.getElementById("sender").style.display = "flex";
    var newtile_ = document.createElement("div");
    var newview_ = document.createElement("div");
    newtile_.textContent = idin_[0];
    newtile_.id = "person_"+idin_[1];
    newview_.id = "viewer_"+idin_[1];
    newview_.className = "viewer division";
    newview_.style.display = "none";
    newview_.textContent = newtile_.textContent;
    newtile_.addEventListener("click",function(){showcurrent(newview_)});
    division_alive.appendChild(newtile_);
    division_viewerpov.appendChild(newview_);
    Spwaned.push(newview_);
}

function showcurrent(user)
{
    document.getElementById("person_"+user.id.split("_")[1]).style.backgroundColor = "rgba(152, 192, 217)";
    document.getElementById("intial_view").style.display="none";
    for (var i = 0;i < Spwaned.length;i++ )
    {
        Spwaned[i].style.display = "none";
    }
    user.style.display = "flex";
    focusedUser = user;
}

function createmessage()
{
    var subDiv_ = document.createElement("div");
    focusedUser.scrollTo = focusedUser.scrollBy(0,100);
    var Content_ = document.getElementById("message").value;
    if (Content_ == "")
        return false;
    subDiv_.textContent = Content_;
    subDiv_.className = "sentmessage";
    subDiv_.id = "message_" + countMessage[focusedUser.id];
    countMessage[focusedUser.id] += 1 ;
    focusedUser.appendChild(subDiv_);
    // document.getElementById("message").value="";
    return "thisisamessage_/!_" + Content_ + "~^~" + focusedUser.id
}

function recievedmessage(recievedata)
{
    var reciever = recievedata.split("~^~")[1];
    recievedata = recievedata.split("~^~")[0];
    var recieverid_ = document.getElementById(reciever);
    if(recieverid_ == null)
    {
        console.error("::recieverid_ is null ",reciever);
        return false;
    }
    if(recieverid_ != focusedUser)
    {
        var tile = document.getElementById("person_"+reciever.split("_")[1]);
        tile.style.backgroundColor = "pink";
    }
    var subDiv_ = document.createElement("div");
    recieverid_.scrollTo=recieverid_.scrollBy(0,100);
    subDiv_.textContent =recievedata;
    subDiv_.className="recievedmessage";
    subDiv_.id = "message_"+countMessage;
    countMessage++;
    recieverid_.appendChild(subDiv_);
}
// ------------------------------------------------------------------------------------------------

document.addEventListener("DOMContentLoaded", function(event) {
    eventlisteners();
    recievedataFromPython();
});