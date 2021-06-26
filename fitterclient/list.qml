import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2

Rectangle 
{
    visible: true
    height: 500
    width : 700
    id : list_view

    Component.onCompleted:{
        console.log(L.noun_cnt())
    }

    Column {
        id: column
        x: 8
        y: 61
        width: 200
        height: 400

        Rectangle {
            id: rectangle
            width: 200
            height: 20
            color: "#fd3f66"
        }

        Rectangle {
            id: rectangle1
            width: 200
            height: 20
            color: "#00ffaa"
        }

        Rectangle {
            id: rectangle2
            width: 200
            height: 20
            color: "#f1f3af"
        }
    }
}
