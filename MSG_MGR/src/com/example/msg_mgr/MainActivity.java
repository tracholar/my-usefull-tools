package com.example.msg_mgr;

import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.Date;
import java.text.SimpleDateFormat;

import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.app.Activity;
import android.database.Cursor;
import android.database.sqlite.SQLiteException;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.widget.Chronometer;
import android.widget.TextView;

public class MainActivity extends Activity {

	final String SMS_URI_ALL = "content://sms/";  
    final String SMS_URI_INBOX = "content://sms/inbox";  
    final String SMS_URI_SEND = "content://sms/sent";  
    final String SMS_URI_DRAFT = "content://sms/draft";  
    final String SMS_URI_OUTBOX = "content://sms/outbox";  
    final String SMS_URI_FAILED = "content://sms/failed";  
    final String SMS_URI_QUEUED = "content://sms/queued";  
    
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        TextView tv = (TextView) findViewById(R.id.tv);
        tv.setText(getMsg());
    }
    
    private String getMsg(){
    	StringBuffer strbf = new StringBuffer(1024);
    	
    	try{
    		Uri uri = Uri.parse(SMS_URI_ALL);
    		String[] projection = new String[] {"_id", "address",
    			"person", "body", "date", "type"};
    		Cursor cur = getContentResolver().query(uri, projection, null, null, "date desc");
    		int nrow = 0;
    		if(cur.moveToFirst()){
    			int iaddress = cur.getColumnIndex("address");
    			int iperson = cur.getColumnIndex("person");
    			int ibody = cur.getColumnIndex("body");
    			int idate = cur.getColumnIndex("date");
    			int itype = cur.getColumnIndex("type");
    			
    			do{
    				String saddr = cur.getString(iaddress);
    				int intPerson = cur.getInt(iperson);
    				String strbodyString = cur.getString(ibody);
    				long longDate = cur.getLong(idate);  
                    int intType = cur.getInt(itype);  
                    
                    SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                    Date date = new Date(longDate);
                    String strDateString = dateFormat.format(date);
                    
                    String strTypeString = null;
                    if(intType == 1){
                    	strTypeString = "接收";
                    }else if (intType == 2) {
						strTypeString = "发送";
					}else{
						strTypeString = Integer.toString(intType);
					}
                    
                    strbf.append(saddr + ",");
                    strbf.append(strTypeString + ",");
                    strbf.append(intPerson + ",");
                    strbf.append(strbodyString + ",");
                    strbf.append(strDateString + "\n\n");
                    
                    nrow += 1;
    			}while(nrow < 100 && cur.moveToNext());
    		}
    	}catch(SQLiteException e){
    		strbf.append("SQLiteException in getSmsInPhone" + e.getMessage());
    	}
    	
    	return strbf.toString();
    }

    private void saveMsg(){
    	
    	
    	try{
    		Uri uri = Uri.parse(SMS_URI_ALL);
    		String[] projection = new String[] {"_id", "address",
    			"person", "body", "date", "type"};
    		Cursor cur = getContentResolver().query(uri, projection, null, null, "date desc");
    		
    		File sdCard = Environment.getExternalStorageDirectory();
    		
    		File dirFile = new File(sdCard.getAbsolutePath() + "/MSG_MGR");
    		if(!dirFile.exists()){
    			dirFile.mkdirs();
    		}
    		SimpleDateFormat formatter = new SimpleDateFormat("yyyyMMddHHmmss");
    		String t = formatter.format(System.currentTimeMillis());
    		File file = new File(dirFile, "msg" + t + ".csv");
    		//FileOutputStream fs = new FileOutputStream(file);
    		FileWriter fs = new FileWriter(file);
    		
    		int nrow = 0;
    		if(cur.moveToFirst()){
    			int iaddress = cur.getColumnIndex("address");
    			int iperson = cur.getColumnIndex("person");
    			int ibody = cur.getColumnIndex("body");
    			int idate = cur.getColumnIndex("date");
    			int itype = cur.getColumnIndex("type");
    			
    			do{
    				StringBuffer strbf = new StringBuffer(1024);
    				
    				String saddr = cur.getString(iaddress);
    				int intPerson = cur.getInt(iperson);
    				String strbodyString = cur.getString(ibody);
    				long longDate = cur.getLong(idate);  
                    int intType = cur.getInt(itype);  
                    
                    SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-mm-dd hh:mm:dd");
                    Date date = new Date(longDate);
                    String strDateString = dateFormat.format(date);
                    
                    String strTypeString = null;
                    if(intType == 1){
                    	strTypeString = "接收";
                    }else if (intType == 2) {
						strTypeString = "发送";
					}else{
						strTypeString = Integer.toString(intType);
					}
                    
                    strbf.append(saddr + Character.toString((char)2));
                    strbf.append(strTypeString + Character.toString((char)2));
                    strbf.append(intPerson + Character.toString((char)2));
                    strbf.append(strbodyString + Character.toString((char)2));
                    strbf.append(strDateString + Character.toString((char)1));
                    
                    
                    fs.write(strbf.toString());
                    
                    nrow += 1;
    			}while(cur.moveToNext());
    			
    			fs.close();
    			
    		}
    	}catch(Exception e){
    		TextView tv = (TextView) findViewById(R.id.tv);
    		tv.append("Exception in save message " + e.getMessage()+"\n");
    	}
    	
    }

    public void onBtClick(View v){
    	TextView tv = (TextView) findViewById(R.id.tv);
    	tv.setText("");
    	tv.setText("正在导出短信到文件...\n");
    	saveMsg();
    	tv.append("导出结束！\n");
    }
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }
    
}
