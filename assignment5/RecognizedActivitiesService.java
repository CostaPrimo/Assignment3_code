package com.example.assignment5;

import android.app.IntentService;
import android.content.Intent;
import androidx.annotation.Nullable;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;
import com.google.android.gms.location.ActivityRecognitionResult;
import com.google.android.gms.location.DetectedActivity;
import java.util.ArrayList;

public class RecognizedActivitiesService extends IntentService {

    public RecognizedActivitiesService() {
        super("RecognizedActivitiesService");
    }

    @Override
    protected void onHandleIntent(@Nullable Intent intent) {
        ActivityRecognitionResult result = ActivityRecognitionResult.extractResult(intent);
        ArrayList<DetectedActivity> activities = (ArrayList<DetectedActivity>) result.getProbableActivities();
        for(DetectedActivity activity : activities){
            Intent intent1 = new Intent(MainActivity.BROADCAST_ACTIVITY_RECOGNITION);
            intent1.putExtra("type", activity.getType());
            intent1.putExtra("confidence", activity.getConfidence());
            LocalBroadcastManager.getInstance(this).sendBroadcast(intent1);
        }
    }
}
