void vibratorWarning(int side, byte intensity, int interval){
  for (byte i; i<intensity; i++){
    if (side == 7){
      digitalWrite(vibratorLeft,LOW);
      digitalWrite(vibratorRight, HIGH);
      delay(interval);
      digitalWrite(vibratorRight, LOW);
      digitalWrite(vibratorLeft,LOW);
      }
    else{
      digitalWrite(side,HIGH);
      delay(interval);
      digitalWrite(side,LOW);
       }
    }
}

byte setUserType(){
  byte userType;
  if (dbButtonLeft.fell()){
    buttonTimer = millis();
    timerOn = true;
    }
  if (dbButtonLeft.rose()){
    buttonPressLeft = (millis() - buttonTimer);
    timerOn = false;
    }
  else{
    if (dbButtonRight.fell()){
      buttonTimer = millis();
      timerOn = true;
      }
    if (dbButtonRight.rose()){
      buttonPressRight = (millis() - buttonTimer);
      timerOn = false;
      }
    }
  if (buttonPressLeft > 0 && buttonPressLeft <= 250){
    userType = assistedMode // case 1
    buttonPressLeft = 0;
    digitalWrite(vibradorRight,
    }
  if (timerOn == true && (millis() - buttonPressLeft) > 2000){
    userType = assistedMode;
    iniciarTimer = false;
    buttonPressLeft = 0;
    }
  else{
    if (buttonPressLeft > 0 && buttonPressLeft <= 250){
      userType = ;
      duracaoBotaoApertado = 0;
      }
    if (timerOn == true && (millis() - buttonPress) > 2000){
      userType = assistedMode;
      iniciarTimer = false;
      buttonPress = 0;
      }
    }   
  return userType;
}

void setUserConfig(){
  userType = setUserType;
  switch (setUserType){
    
    case botaoNormalDireito:
      if (botaoNormalAtivo){
        contarApertosNormaisDireito++;
        }
      break;
  
    case botaoLongoDireito:
      contadorApertosLongosDireito++;
      if (contadorApertosLongosDireito == 1){
          retomarCaseZero = false;
          botaoNormalAtivo = true;
          lcd.clear();
          digitalWrite(ledFaixa, LOW);
          usuarioDesligou = true;
          printLCD(2,2,"Faixa desativada");
          }
      if (contadorApertosLongosDireito == 2) {
        digitalWrite(led, LOW);
        retomarCaseZero = true;
        botaoNormalAtivo = false;
        contadorApertosLongosDireito = 0;
        lcd.clear();
        }
      break;
  
    case semRespostaDireito:
      if (retomarCaseZero == true){
        printLCD(1,1,"CM");
        }
    }
}
