import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2

Rectangle 
{
    visible: true
    height: 500
    width : 700
    id : the_window
    
    TextInput {
        id: target_ip
        x: 118
        y: 177
        width: 187
        height: 28
        text: qsTr("ip")
        font.pixelSize: 12
    }

    Button {
        id: button
        x: 328
        y: 177
        width: 82
        height: 28
        text: qsTr("Button")
        font.family: "Tahoma"
        onClicked:{
            console.log(target_ip.text)
            var compMainPage = Qt.createComponent("test2.qml")
            .createObject(the_window, {x:0, y:0, width:500, height:700});
 
        }
    }
    
}
