package com.example.fg;
import org.tensorflow.lite.DataType;
import org.tensorflow.lite.Interpreter;
import org.tensorflow.lite.gpu.GpuDelegate;
import org.tensorflow.lite.support.image.ImageProcessor;
import org.tensorflow.lite.support.image.TensorImage;
import org.tensorflow.lite.support.image.ops.ResizeOp;
import org.tensorflow.lite.support.tensorbuffer.TensorBuffer;

import android.content.res.AssetFileDescriptor;
import android.graphics.Bitmap;
import android.content.res.AssetFileDescriptor;

import android.content.res.AssetManager;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;

public class Classifier {
    /*private ImageProcessor dataProcessor =
            new ImageProcessor.Builder()
                    .add(new ResizeOp(224, 224, ResizeOp.ResizeMethod.BILINEAR))
                    .build();


*/
    static float[][][][] reshapeToFourDimension(float[] arr,int size1,int size2, int size3){
        float[][][][] newArr = new float[size1][size2][size3][1];
        int index=0;

        for(int i=0; i<size1; i++){
            for(int j=0; j<size2; j++){
                for(int k=0; k<size3; k++) {
                    newArr[i][j][k][0] = arr[index];
                    index++;
                }
            }
        }
        return newArr;
    }


    // Create a TensorImage object, this creates the tensor the TensorFlow Lite
    // interpreter needs
    //private TensorImage data = new TensorImage(DataType.UINT8);

    static MappedByteBuffer loadModelFile(AssetManager assetManager, String modelPath) throws IOException {
        AssetFileDescriptor fileDescriptor = assetManager.openFd(modelPath);
        FileInputStream inputStream = new FileInputStream(fileDescriptor.getFileDescriptor());
        FileChannel fileChannel = inputStream.getChannel();
        long startOffset = fileDescriptor.getStartOffset();
        long declaredLength = fileDescriptor.getDeclaredLength();
        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength);
    }

    // Analysis code for every frame
    // Preprocess the image
/*
     //  data.load(bitmap);
    data = dataProcessor.process(data);

    //Running inference


*/

}

