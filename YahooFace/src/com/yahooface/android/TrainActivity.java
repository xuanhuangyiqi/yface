package com.yahooface.android;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

import org.json.JSONException;
import org.json.JSONObject;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.Button;
import android.widget.GridView;
import android.widget.TextView;

import com.yahooface.http.HttpTask;

public class TrainActivity extends UpdateActivity{  
     GridView gridView_check;        //多选宫格    
     Button trainbtn;
     ImageAndTextListAdapter ia_check;            //存储图片源的适配器(多选)    
     TextView yahooname;
          
     /** Called when the activity is first created. */ 
     @Override 
     public void onCreate(Bundle savedInstanceState) {    
             super.onCreate(savedInstanceState);    
             setContentView(R.layout.train);    
             
             yahooname = (TextView)findViewById(R.id.yahooname);
             yahooname.setText(Account.getUser());
             // 多选的宫格     
//             gridView_check = (GridView) findViewById(R.id.gridview);    
//             ia_check = new ImageAdapter(this, true);    
//             gridView_check.setAdapter(ia_check);    
//             // 设置点击监听     
//             gridView_check.setOnItemClickListener(new OnItemClickListener() {    
//                     @Override 
//                     public void onItemClick(AdapterView<?> arg0, View arg1,    
//                                     int position, long arg3) {    
//                             // TODO Auto-generated method stub    
//                             ia_check.changeState(position);    
//                     }    
//             }); 
             //多选的宫格     
            gridView_check = (GridView)findViewById(R.id.gridview);  
            trainbtn = (Button)findViewById(R.id.trainbtn);
     		List<ImageAndText> list = new ArrayList<ImageAndText>();
     		for(int i=0;i<Account.urls.length;i++)
	    		list.add(new ImageAndText(TrainActivity.this.getResources().getString(R.string.serverip)+Account.urls[i],"头像"+String.valueOf(i+1)));
    		
    		ia_check = new ImageAndTextListAdapter(this,this, list, gridView_check);
    		gridView_check.setAdapter(ia_check);   
             // 设置点击监听     
             gridView_check.setOnItemClickListener(new OnItemClickListener() {    
                     @Override 
                     public void onItemClick(AdapterView<?> arg0, View arg1,    
                                     int position, long arg3) {    
                             // TODO Auto-generated method stub    
                             ia_check.changeState(position);    
                     }    
             }); 
             trainbtn.setOnClickListener(new OnClickListener() {
				
				@Override
				public void onClick(View v) {
					// TODO Auto-generated method stub
					StringBuilder sb= new StringBuilder();
					String title="Training...";
					HttpTask task = new HttpTask(TrainActivity.this,TrainActivity.this,title);
					JSONObject jsob = null;
					String jsobstr = null;
					for(int i=0;i<ia_check.mImage_bs.size();i++)
					{
						if(ia_check.mImage_bs.get(i))
						{
							sb.append(TrainActivity.this.getResources().getString(R.string.serverip)+Account.urls[i]+",");
						}
						//sb = sb.subSequence(0, sb.length()-2);
						JSONObject obj = new JSONObject();
			    		try {
							obj.put("images", sb.toString());
							System.out.println(obj.toString());
						} catch (JSONException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}

						try {
							jsob =  new JSONObject();
							jsob.put("images", sb.toString().substring(0, sb.toString().length()-2));
							jsobstr = java.net.URLEncoder.encode(jsob.toString(),"utf-8");
						} catch (Exception e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
						//Toast.makeText(getApplicationContext(), String.valueOf(i)+": "+String.valueOf(ia_check.mImage_bs.elementAt(i)), Toast.LENGTH_SHORT).show();
					}
					String url = TrainActivity.this.getResources().getString(R.string.serverip)+TrainActivity.this.getResources().getString(R.string.trainurl)+"?username="+Account.getUser()+"&avatars="+jsobstr;
					Log.v("url",url);
					task.execute("POST",url);  
					//训练完成之后，需要将Account.trained设为true
					Intent intent = new Intent(TrainActivity.this,CameraActivity.class);
					startActivity(intent);
					TrainActivity.this.finish();
				}
			});
     }

	@Override
	public void update() {
		// TODO Auto-generated method stub
		
	}    
	
}
