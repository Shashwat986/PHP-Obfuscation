<?PHP
	$fromAngle = $_GET['f'];
	$toAngle = $_GET['t'];
	$increase = false;
	echo 'from: ' . $fromAngle . ', to: ' . $toAngle . '<br />';
	echo '-------------------------<br />';
	echo $fromAngle . '<br />';
	
	
	if ($fromAngle < $toAngle) $increase = true; // <--------------- YOUR ALGORITM
	
	while($fromAngle != $toAngle){
		$fromAngle = ($increase) ? $fromAngle + 10 : $fromAngle - 10;

		if($fromAngle > 180) $fromAngle = -170;
		if($fromAngle < -170) $fromAngle = 180;

		$newAngle = $fromAngle;
		if($fromAngle == 40 || $fromAngle == -40 || $fromAngle == 140 || $fromAngle == -140)
			$newAngle -= 10;
			
		echo $newAngle . '<br />';
	}
?>