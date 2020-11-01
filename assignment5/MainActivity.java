package com.example.assignment5;

import androidx.appcompat.app.AppCompatActivity;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import com.google.android.gms.location.DetectedActivity;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private ArrayList<String> readings = new ArrayList<String>();

    private BroadcastReceiver broadcastReceiver = null;
    public static String BROADCAST_ACTIVITY_RECOGNITION = "activity_recognition";
    public static int DETECTION_INTERVAL_IN_MILLISECONDS = 5000;

    private File path = null;
    private File file = null;

    TextView activityText;
    TextView timerText;
    Button readbtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        path = this.getFilesDir();
        file = new File(path, "ActivityData.txt");
        if(!file.exists()){
            try {
                Log.e("Created", ""+file.createNewFile());

            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        activityText = (TextView)findViewById(R.id.activitydisplay);
        timerText = (TextView)findViewById(R.id.timer);
        readbtn = (Button)findViewById(R.id.readbtn);

        readbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    //saveData(readings, MainActivity.this);
                    showLoggedData(MainActivity.this);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
            }
        });

        broadcastReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                if(intent.getAction() == (MainActivity.BROADCAST_ACTIVITY_RECOGNITION)){
                    int type = intent.getIntExtra("type", -1);
                    int confidence = intent.getIntExtra("confidence", 0);
                    handleUserActivity(type, confidence);
                }
            }
        };
        Intent intent = new Intent(this, BackgroundRecognizedActivitiesService.class);
        startService(intent);
    }

    private void handleUserActivity(int type, int confidence){
        String activityType;
        switch(type) {
            case DetectedActivity.STILL:
                activityType = "Still";
                break;
            case DetectedActivity.ON_FOOT:
                activityType = "On Foot";
                break;
            case DetectedActivity.WALKING:
                activityType = "Walking";
                break;
            case DetectedActivity.RUNNING:
                activityType = "Running";
                break;
            case DetectedActivity.IN_VEHICLE:
                activityType = "In vehicle";
                break;
            case DetectedActivity.ON_BICYCLE:
                activityType = "On Bicycle";
                break;
            case DetectedActivity.TILTING:
                activityType = "Tilting";
                break;
            default:
                activityType = "Unknown Activity";
                break;
        }
        if(confidence>70){
            activityText.setText(activityType);
            timerText.setText(""+confidence);
            readings.add(System.currentTimeMillis()+","+activityType+","+confidence);
            Log.e("Data", "Saved");
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        LocalBroadcastManager.getInstance(this).registerReceiver(broadcastReceiver, new IntentFilter(BROADCAST_ACTIVITY_RECOGNITION));
    }

    @Override
    protected void onPause() {
        super.onPause();
        LocalBroadcastManager.getInstance(this).unregisterReceiver(broadcastReceiver);
    }

    private void saveData(ArrayList<String> data, Context context){
        try {
            FileOutputStream stream = new FileOutputStream(file);
            OutputStreamWriter mStream = new OutputStreamWriter(stream);
            for(String read: readings) {
                mStream.append(read).append('\n');
            }
            mStream.close();
            stream.close();
            Log.e("Data Written", "..");
        }
        catch (IOException e) {
            Log.e("Exception", "File write failed: " + e.toString());
        }
    }

    private void saveData(String data, Context context){
        try {
            FileOutputStream stream = new FileOutputStream(file);
            OutputStreamWriter mStream = new OutputStreamWriter(stream);
            mStream.append(data).append('\n');
            mStream.close();
            stream.close();
            Log.e("Data Written", "..");
        }
        catch (IOException e) {
            Log.e("Exception", "File write failed: " + e.toString());
        }
    }

    private void showLoggedData(Context context) throws FileNotFoundException {
        FileInputStream fis = context.openFileInput("ActivityData.txt");
        InputStreamReader inputStreamReader = new InputStreamReader(fis, StandardCharsets.UTF_8);
        StringBuilder stringBuilder = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(inputStreamReader)) {
            String line = reader.readLine();
            while (line != null) {
                stringBuilder.append(line).append('\n');
                line = reader.readLine();
            }
            inputStreamReader.close();
            fis.close();
        } catch (IOException e) {
            // Error occurred when opening raw file for reading.
        } finally {
            for(String reading: readings){
                stringBuilder.append(reading).append('\n');
            }
            readings.clear();
            String contents = stringBuilder.substring(0);
            saveData(contents, context);
            Log.e("File", contents);
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        //saveData(readings, this);
    }
}