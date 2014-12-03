package com.google.vrtoolkit.cardboard.samples.treasurehunt;

/**
 * Created by squirrelrao on 14-12-3.
 */
public class User {

    private String ip;
    private float[] headPosition = new float[]{0f,0f,0f};

    public String getIp() {
        return ip;
    }

    public void setIp(String ip) {
        this.ip = ip;
    }

    public float[] getHeadPostion(){
        return headPosition;
    }

    public void setHeadPosition(float[] position){
        this.headPosition = position;
    }
}
