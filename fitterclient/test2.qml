import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2

Rectangle 
{
    visible: true
    height: 500
    width : 700
    id : another_page
    
    Text {
        x: 118
        y: 177
        width: 187
        height: 28
        text: qsTr("heloo!!!!!!")
        font.pixelSize: 12
    }
}
