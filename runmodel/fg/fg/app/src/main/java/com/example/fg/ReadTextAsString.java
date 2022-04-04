package com.example.fg;

import android.os.Build;

import androidx.annotation.RequiresApi;



import java.io.File;
import java.nio.file.Paths;

import static java.nio.file.Files.readAllBytes;

public class ReadTextAsString {
    @RequiresApi(api = Build.VERSION_CODES.O)
    public static String readFileAsString(String fileName) throws Exception {
        String data = "";
        data = new String(readAllBytes(Paths.get(fileName)));
        return data;
    }
}
