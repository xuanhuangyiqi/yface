package com.yahooface.android;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.yahooface.http.HttpTask;

public class PersonInfoActivity extends UpdateActivity {

	private Button registerbtn;
	private TextView aboutmename;
	private TextView yahooname;
	private EditText yahooid;
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		// TODO Auto-generated method stub
		super.onCreate(savedInstanceState);
		setContentView(R.layout.personinfo);
		
		registerbtn = (Button)findViewById(R.id.register);
		aboutmename = (TextView)findViewById(R.id.aboutmename);
		yahooname = (TextView)findViewById(R.id.yahooname);
		yahooid = (EditText)findViewById(R.id.yahooid);
		yahooname.setText(Account.getUser());
		yahooid.setText(Account.getUser());
		registerbtn.setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
				//Intent intent = new Intent(PersonInfoActivity.this,TrainActivity.class);
				//startActivity(intent);
				connect();
			}
		});
	}
	private void connect() { 
    	Log.v("connect called in PersonInfoActiviy","connect called");
    	String name = aboutmename.getText().toString();
    	if(name.length()==0)
    	{
    		Toast.makeText(getApplicationContext(), "Please input the about.me name", Toast.LENGTH_SHORT).show();
    		return;
    	}
    	String title="Analying images of your flickr \n album, This process may take several\n minites,Please wait patiently,...";
        HttpTask task = new HttpTask(this,this,title); 
        String url = this.getResources().getString(R.string.serverip)+this.getResources().getString(R.string.registerurl)+"?username="+Account.getUser()+"&about_id="+name;
        //System.out.println("login post url: "+url);
        task.execute("POST",url);   
    }
	
	@Override
	public void update() {
		// TODO Auto-generated method stub
		Log.v("update called","update called");
		Intent intent = new Intent(PersonInfoActivity.this,TrainActivity.class);
		startActivity(intent);
		this.finish();
	} 

}
