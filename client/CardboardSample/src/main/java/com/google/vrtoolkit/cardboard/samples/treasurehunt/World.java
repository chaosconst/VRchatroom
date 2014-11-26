package com.google.vrtoolkit.cardboard.samples.treasurehunt;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by yuan on 14-11-25.
 */
public class World {
    Map<String, float[]> map = new HashMap<String, float[]>();

    synchronized void update(String key, float[] value) {
        map.put(key, value);
    }

    synchronized float[] get(String key ) {
        return map.get(key);
    }

}

