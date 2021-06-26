import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2

Rectangle 
{
    visible: true
    height: 500
    width : 700
    id : the_window
    
    Button {
        id: enter_button
        x: 328
        y: 177
        width: 82
        height: 28
        text: qsTr("Enter")
        font.pointSize: 12
        focusPolicy: Qt.NoFocus
        font.family: "Arial"
        onClicked:{
            if ( L.connect(input_ip.text , input_port.text) ){
                var list_view = Qt.createComponent("list.qml").createObject(the_window)
            }
        }
    }

    TextInput {
        id: input_ip
        x: 83
        y: 124
        width: 187
        height: 28
        text: qsTr("127.0.0.1")
        font.pixelSize: 15
    }


    TextInput {
        id: input_port
        x: 83
        y: 177
        width: 187
        height: 28
        text: qsTr("7899")
        font.pixelSize: 15
    }
    
}
