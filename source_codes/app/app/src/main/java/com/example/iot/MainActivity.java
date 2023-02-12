package com.example.iot;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.StringRes;
import androidx.appcompat.app.AppCompatActivity;

import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.content.res.Resources;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.view.View;
import android.widget.HeaderViewListAdapter;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;

import java.util.HashMap;
import java.util.Map;
import com.loopj.android.http.*;
import cz.msebera.android.httpclient.Header;
import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import okhttp3.ResponseBody;
import static java.lang.System.out;

public class MainActivity extends AppCompatActivity {

    protected static final int RESULT_SPEECH = 1;
    private ImageButton btnSpeak;
    private TextView tvText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        tvText = findViewById(R.id.tvText);
        btnSpeak = findViewById(R.id.btnSpeak);
        btnSpeak.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "en-US");
                try {
                    startActivityForResult(intent, RESULT_SPEECH);
                    tvText.setText("");
                } catch (ActivityNotFoundException e){
                    Toast.makeText(getApplicationContext(), "Your device doesn't support Speech to Text", Toast.LENGTH_SHORT).show();

                    e.printStackTrace();
                }
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        switch (requestCode){
            case RESULT_SPEECH:
                if(resultCode == RESULT_OK && data != null){
                    ArrayList<String> text = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
                    tvText.setText(text.get(0));
//                    AsyncHttpClient client = new AsyncHttpClient();
//                    client.get("http://129.236.229.142:8010", new AsyncHttpResponseHandler() {
//                    String url = "http://129.236.229.142:8010" +"/?msg=" + text.get(0);
//
//                        @Override
//                        public void onSuccess(int statusCode, Header[] headers, byte[] response) {
//
//
//
//
//                            // called when response HTTP status is "200 OK"
//                        }
//
//                        @Override
//                        public void onFailure(int statusCode, Header[] headers, byte[] errorResponse, Throwable e) {
//                            Toast.makeText(getApplicationContext(), "Your device doesn't support Speech to Text", Toast.LENGTH_SHORT).show();
//                            // called when response HTTP status is "4XX" (eg. 401, 403, 404)
//                        }
//                    });
                    String url = "https://d921-129-236-229-142.ngrok.io?msg=" + text.get(0);
                    OkHttpClient client = new OkHttpClient();
                        Request request = new Request.Builder()
                                .url(url)
                                .build();
//                    MediaType MEDIA_TYPE_MARKDOWN = MediaType.parse("text/x-markdown; charset=utf-8");
//
//                    OkHttpClient client = new OkHttpClient();
//
//
//                    String postBody = ""
//                            + "Releases\n"
//                            + "--------\n"
//                            + "\n"
//                            + " * _1.0_ May 6, 2013\n"
//                            + " * _1.1_ June 15, 2013\n"
//                            + " * _1.2_ August 11, 2013\n";
//
//                    Request request = new Request.Builder()
//                            .url("https://129.236.229.142:8010")
//                            .post(RequestBody.create(MEDIA_TYPE_MARKDOWN, postBody))
//                            .build();
                    client.newCall(request).enqueue(new Callback() {
                        @Override
                        public void onFailure(@NonNull Call call, @NonNull IOException e) {
                            e.printStackTrace();
                        }

                        @Override
                        public void onResponse(@NonNull Call call, @NonNull Response response) throws IOException {
                            if (response.isSuccessful()){
                                final String myResponse = response.body().string();

                                MainActivity.this.runOnUiThread(new Runnable() {
                                    @Override

                                    public void run() {
                                        System.out.println(myResponse);
                                    }
                                });
                            }

                        }
                    });
//
                    /*try (Response response = client.newCall(request).execute()) {
                        if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);
                        System.out.println(response.body().string());
                    } catch (IOException e) {
                        e.printStackTrace();
                    }*/



                }
            break;
        }
    }

//   private void serverSend(String url, text.get(0)){
//        AsyncHttpClient client = new AsyncHttpClient();
//        client.get("http://129.236.229.150:8010", new AsyncHttpResponseHandler() {
//            String url = "http://129.236.229.150:8010" + text.get(0);
//
//            @Override
//            public void onSuccess(int statusCode, Header[] headers, byte[] response) {
//
//
//
//
//                // called when response HTTP status is "200 OK"
//            }
//
//            @Override
//            public void onFailure(int statusCode, Header[] headers, byte[] errorResponse, Throwable e) {
//                Toast.makeText(getApplicationContext(), "Your device doesn't support Speech to Text", Toast.LENGTH_SHORT).show();
//                // called when response HTTP status is "4XX" (eg. 401, 403, 404)
//            }
//        });
//    }

}