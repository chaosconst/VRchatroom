package com.google.vrtoolkit.cardboard.samples.treasurehunt;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

/**
 * Created by yuan on 14-11-25.
 */
public class World {
    Map<String, float[]> map = new HashMap<String, float[]>();

    Map<String,User> userMap = new HashMap<String,User>();

    private int onlineUserCount = 0;

    synchronized void update(String key, float[] value) {
        map.put(key, value);
    }

    synchronized float[] get(String key ) {
        return map.get(key);
    }

    synchronized User getUser(String key){


        return  userMap.get(key);
    }

    synchronized void updateUser(User user){
        userMap.put(user.getIp().trim(),user);
    }

    synchronized List<User> getOnlineUsers(){

         List<User> users = new ArrayList<User>();
         Iterator<String> keys = this.userMap.keySet().iterator();
         while(keys.hasNext()){
             String key = keys.next();
             users.add(this.userMap.get(key));
         }
        onlineUserCount = users.size();
        return users;
    }



}

