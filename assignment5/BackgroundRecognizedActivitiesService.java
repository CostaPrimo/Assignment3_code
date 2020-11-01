package com.example.assignment5;

import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.os.Binder;
import android.os.IBinder;
import android.util.Log;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.google.android.gms.location.ActivityRecognitionClient;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;

public class BackgroundRecognizedActivitiesService extends Service {

    public BackgroundRecognizedActivitiesService(){
    }

    private Intent mIntent = null;
    private PendingIntent pendingIntent = null;
    private ActivityRecognitionClient activityRecognitionClient = null;
    protected IBinder mBinder = new LocalBinder();

    class LocalBinder extends Binder {
        BackgroundRecognizedActivitiesService service = BackgroundRecognizedActivitiesService.this;
    }

    @Override
    public void onCreate() {
        super.onCreate();
        activityRecognitionClient = new ActivityRecognitionClient(this);
        mIntent = new Intent(this, RecognizedActivitiesService.class);
        pendingIntent = PendingIntent.getService(this, 1, mIntent, PendingIntent.FLAG_UPDATE_CURRENT);
        startActivityUpdates();
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return mBinder;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        super.onStartCommand(intent, flags, startId);
        return START_STICKY;
    }

    private void startActivityUpdates(){
        Task<Void> activityUpdates = activityRecognitionClient.requestActivityUpdates(MainActivity.DETECTION_INTERVAL_IN_MILLISECONDS, pendingIntent);
        activityUpdates.addOnSuccessListener(new OnSuccessListener<Void>() {
            @Override
            public void onSuccess(Void aVoid) {
                Log.e("TEST_A", "Start Activity Updates Success");
            }
        });
        activityUpdates.addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull Exception e) {
                Log.e("TEST_B", "Start Activity Updates Fail");
            }
        });
    }

    private void stopActivityUpdates(){
        Task<Void> activityUpdates = activityRecognitionClient.removeActivityUpdates(pendingIntent);
        activityUpdates.addOnSuccessListener(new OnSuccessListener<Void>() {
            @Override
            public void onSuccess(Void aVoid) {
                Log.e("TEST_C", "Stop Activity Updates Success");
            }
        });
        activityUpdates.addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull Exception e) {
                Log.e("TEST_D", "Stop Activity Updates Fail");
            }
        });
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        stopActivityUpdates();
    }
}
