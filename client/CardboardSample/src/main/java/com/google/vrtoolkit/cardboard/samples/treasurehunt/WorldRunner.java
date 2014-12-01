package com.google.vrtoolkit.cardboard.samples.treasurehunt;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import android.util.Log;
import org.json.*;

/**
 * Created by yuan on 14-11-25.
 */
public class WorldRunner implements Runnable{

    private static final String TAG = "WorldRunner";

    private World world;
    public boolean KeepWorldRunning = true;


    //related to network
    Socket echoSocket;
    private PrintWriter out ;
    private BufferedReader in;


    public void run() {
        try {
            init();
        } catch (UnknownHostException e) {
//            mOverlayView.show3DToast("Unknow Host, Can't get online!");
        } catch (IOException e) {
//            mOverlayView.show3DToast("Host IO Error, Can't get online!");
        }

        while (KeepWorldRunning) {
            try {
                float[] forward = world.get("HeadVector");
                if (forward!=null) {
                    String headVectorStr = "{\"HeadVector\": [" + forward[0] + ", " + forward[1] + ", " + forward[2] + "]}";
                    out.println(headVectorStr);
                    String positionStr = in.readLine();
                    JSONObject obj = new JSONObject(positionStr);
                    String selfname = obj.getString("self");
                    JSONArray status = obj.getJSONArray(selfname);
                    float[] position = new float[3];
                    position[0] = (float)status.getDouble(3);
                    position[1] = (float)status.getDouble(4);
                    position[2] = (float)status.getDouble(5);
                    world.update("HeadPosition", position);
                    Log.i(TAG, positionStr);
                }
            } catch(Throwable e){
                Log.e(TAG, e.toString());
            }
        }
    }

    public void init() throws UnknownHostException, IOException {
        echoSocket = new Socket("swarma.net", 1920);
        out = new PrintWriter(echoSocket.getOutputStream(), true);
        in = new BufferedReader(
                new InputStreamReader(echoSocket.getInputStream()));
    }

    public void setWorld(World world) {
        this.world = world;
    }
}
