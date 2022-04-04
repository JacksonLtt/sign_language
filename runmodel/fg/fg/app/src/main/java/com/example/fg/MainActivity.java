package com.example.fg;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.content.pm.PackageManager;
import android.content.res.AssetManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import org.tensorflow.lite.DataType;
import org.tensorflow.lite.Interpreter;
import org.tensorflow.lite.gpu.GpuDelegate;
import org.tensorflow.lite.support.model.Model;
import org.tensorflow.lite.support.tensorbuffer.TensorBuffer;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.nio.DoubleBuffer;
import java.nio.channels.FileChannel;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.*;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;

import static java.nio.file.Files.readAllBytes;


public class MainActivity extends AppCompatActivity {
    private Button start;
    ReadTextAsString readtextstring = new ReadTextAsString();
    ByteBuffer bytedata;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //final String[] data = {"hellodfdsf"};
        //System.out.println(data);

        //Path path=Paths.get("test.txt");

        //System.out.println(path);
        /*String current;
        try {
            current = new File(".").getCanonicalPath();
            System.out.println("Current dir:" + current);
        }
        catch  (IOException e) {
            e.printStackTrace();
        }*/
        if (checkSelfPermission(android.Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
            System.out.println("Permission is granted");
            //File write logic here
            //eturn true;
        }
        else
        {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);

        }




        Button button = (Button) findViewById(R.id.startbutton);




        button.setOnClickListener(new View.OnClickListener() {

            @RequiresApi(api = Build.VERSION_CODES.O)
            public void onClick(View v) {
                for (int loop = 0; loop < 100000; loop++) {
                    try {

                        //Path path = Paths.get("C:/scarlett/fingertrack/resnet/test.txt");
                        //InputStream inputStream =  Files.new//  Files.newInputStream(path);
                        //java.io.FileInputStream() fileInputStream =
                        //FileInputStream inputStream  = new FileInputStream("C:\\scarlett\\fingertrack\\resnet\\test.txt");
                        //File myfile = new File(Environment.getExternalStorageDirectory().toString() + "/file.txt");


                        long BeforeTimeload = System.currentTimeMillis();
                        File myfile = new File(Environment.getExternalStorageDirectory().toString() + "/singlefile.txt");
                        System.out.println(Environment.getExternalStorageDirectory().toString());
                        FileInputStream inputStream = new FileInputStream(myfile.getPath());

                        bytedata = loadfiletobuffer.readToByteBuffer(inputStream);
                        long AfterTimeload = System.currentTimeMillis();
                        System.out.println("loadingdata");
                        System.out.println(AfterTimeload - BeforeTimeload);


                        long BeforeTimeprocess = System.currentTimeMillis();
                        // Now let's convert this ByteBuffer to String
                        String converted = new String(bytedata.array(), "UTF-8");
                        //System.out.println("Converted : " + converted);
                        // first we can use parseFloat() method to convert String to Float
                        String[] parts = converted.split("#");
                        bytedata = null;
                        System.gc();
                        converted = null;
                        System.gc();
                        float[] numbers = new float[parts.length];
                        for (int i = 0; i < parts.length; ++i) {
                            numbers[i] = Float.parseFloat(parts[i]);
                        }
                        //System.out.println(numbers[4]);
                        //System.out.println(parts.length);

                        //GpuDelegate delegate = new GpuDelegate();
                        //Interpreter.Options options = (new Interpreter.Options()).addDelegate(delegate);
                        AssetManager assetManager = getAssets();
                        String filename = "converted_model_seq2seq.tflite";
                        //Interpreter interpreter = new Interpreter(Classifier.loadModelFile(assetManager,filename), options);
                        Interpreter interpreter = new Interpreter(Classifier.loadModelFile(assetManager, filename));


                        //float[][][][] newarr = Classifier.reshapeToFourDimension(numbers, 217,1000,8);
                        //float[][] output = new float[217][5000];
                        //long BeforeTime = System.currentTimeMillis();
                        //interpreter.run(newarr, output);
                        //long AfterTime = System.currentTimeMillis();
                        //System.out.println("All");
                        //System.out.println(AfterTime-BeforeTime);

                        float[][][][] newarrsingle = Classifier.reshapeToFourDimension(numbers, 1, 1000, 8);
                        float[][] outputsingle = new float[1][5000];
                        long AfterTimeprocess = System.currentTimeMillis();
                        System.out.println("datapreprocess");
                        System.out.println(AfterTimeprocess - BeforeTimeprocess);


                        long BeforeTime = System.currentTimeMillis();
                        interpreter.run(newarrsingle, outputsingle);
                        long AfterTime = System.currentTimeMillis();
                        System.out.println("Single");
                        System.out.println(AfterTime - BeforeTime);

                        //make the system run 720
                        //for(int i=0; i<500; i++) {
                        //    interpreter.run(newarr, output);
                        //    System.out.println(i);

                        //}

                        //System.out.println(newarr[1][1][1][0]);
                        //System.out.println(output[1][1]);
                        //System.out.println(output[200][4000]);
                        //System.out.println(output[20][1]);
                        //System.out.println(output[27][55]);
                        //System.out.println(output[99][66]);

                        long BeforeTimedelay = System.currentTimeMillis();

                        // Clean up
                        //delegate.close();
                        final Handler handler = new Handler();
                        final long dtime=AfterTime - BeforeTime;
                        // Do something after 5s = 5000ms
                        int d = (int) dtime;

                        //final int delay=100-d;
                        final int delay =Math.max(0, 100-d);
                        Thread.sleep(delay);
                        long AfterTimedelay = System.currentTimeMillis();
                        System.out.println("delay");
                        System.out.println(AfterTimedelay - BeforeTimedelay);




                    } catch(IOException | InterruptedException e){
                        e.printStackTrace();
                    }

                }


                TextView textView = (TextView) findViewById(R.id.text);
                textView.setText("the end");

            }
        });
        System.out.println("end");

    }


}
